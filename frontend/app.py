from flask import Flask, render_template, request, redirect, url_for, flash
import random
import xml.etree.ElementTree as ET  # Correct XML import

app = Flask(__name__)
app.secret_key = 'secret'  # For session and flash messages

# Route for the home page
@app.route('/')
def home():
    return render_template("index.html")

# Route for the About page
@app.route('/about')
def about():
    company_name = "Tech Innovations"
    year_founded = 2020
    about_text = "We are a technology company focused on innovation and sustainability."
    return render_template("about.html", company_name=company_name, year_founded=year_founded, about_text=about_text)

# Route for the Game page
@app.route('/game', methods=['GET', 'POST'])
def game():
    # Session to store the secret number
    if 'number' not in request.args:
        secret_number = random.randint(1, 100)
        return redirect(url_for('game', number=secret_number))
    
    secret_number = int(request.args.get('number'))
    
    if request.method == 'POST':
        guess = int(request.form['guess'])
        
        if guess < secret_number:
            ("Too low! Try again.", 'warning')
        elif guess > secret_number:
            flash("Too high! Try again.", 'warning')
        else:
            flash(f"Congratulations! You guessed the number {secret_number}.", 'success')
            # Reset the game after success
            return redirect(url_for('game'))

    return render_template("game.html", secret_number=secret_number)

@app.route('/test')
def test():
    x = "test1"
    y = "test2"
    z = "test3"
    return render_template("test.html", x=x, y=y, z=z)
# Start the Flask application

@app.route('/show_data')
def show_data():

    name = request.args.get('name')
    email = request.args.get('email')
    return render_template('show_data.html', name=name, email=email)



@app.route('/login')
def login():
    return render_template('Login.html')

# Route for the Login page
@app.route('/auth', methods=['GET'])
def auth():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')

        # Check user credentials from the XML file
        if check_user_credentials(username, password):
        # if(username=='admin'):
            return redirect(url_for('success'))
        else:
            flash("Invalid username or password.", 'danger')
            return redirect(url_for('login'))

def check_user_credentials(username, password):
    try:
        tree = ET.parse('users.xml')  # Ensure the path to users.xml is correct
        root = tree.getroot()

        for user in root.findall('user'):
            stored_username = user.find('username').text
            stored_password = user.find('password').text
            
            if username == stored_username and password == stored_password:
                return True
        return False
    except ET.ParseError as e:
        flash(f"XML Parse Error: {e}", 'danger')
        return False
    except FileNotFoundError as e:
        flash(f"File Not Found: {e}", 'danger')
        return False
    except Exception as e:
        flash(f"Error: {e}", 'danger')
        return False

# Success route
@app.route('/success')
def success():
    return render_template('success.html')




# Route to render the "Add User" form
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['new_username']
        password = request.form['new_password']
        
        # Check if username already exists
        if check_username_exists(username):
            flash("Username already exists.", 'danger')
            return redirect(url_for('add_user'))
        
        # Add new user to the XML file
        add_user_to_xml(username, password)
        
        flash("User added successfully.", 'success')
        return redirect(url_for('login'))
    
    return render_template('add_user.html')

# Function to check if the username already exists in the XML file
def check_username_exists(username):
    try:
        tree = ET.parse('users.xml')
        root = tree.getroot()

        for user in root.findall('user'):
            stored_username = user.find('username').text
            if username == stored_username:
                return True
        return False
    except Exception as e:
        flash(f"Error: {e}", 'danger')
        return True

# Function to add the new user to the XML file
def add_user_to_xml(username, password):
    try:
        tree = ET.parse('users.xml')
        root = tree.getroot()

        # Create a new user element
        new_user = ET.Element('user')
        username_elem = ET.SubElement(new_user, 'username')
        password_elem = ET.SubElement(new_user, 'password')
        
        username_elem.text = username
        password_elem.text = password

        # Add the new user to the root
        root.append(new_user)

        # Save the updated XML back to the file
        tree.write('users.xml')
    except Exception as e:
        flash(f"Error adding user to XML: {e}", 'danger')



# Start the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
