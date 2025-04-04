from flask import Flask, render_template, request, redirect, url_for, flash
import random
import xml.etree.ElementTree as ET  # Correct XML import

app = Flask(__name__)
app.secret_key = 'secret'  # For session and flash messages


# ================================================================
# Route for the home page
# ----------------------------------------------------------------

@app.route('/')
def home():
    return render_template("index.html")

# ================================================================
# Route for the About page
# ----------------------------------------------------------------
@app.route('/about')
def about():
    company_name = "Tech Innovations"
    year_founded = 2020
    about_text = "We are a technology company focused on innovation and sustainability."
    return render_template("about.html", company_name=company_name, year_founded=year_founded, about_text=about_text)

# ================================================================
# Route for the Game page
# ----------------------------------------------------------------
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
            flash("Too low! Try again.", 'warning')
        elif guess > secret_number:
            flash("Too high! Try again.", 'warning')
        else:
            flash(f"Congratulations! You guessed the number {secret_number}.", 'success')
            # Reset the game after success
            return redirect(url_for('game'))

    return render_template("game.html", secret_number=secret_number)

# ================================================================
# Route for main1
# ----------------------------------------------------------------
@app.route('/main1')
def main1():
    return render_template("main1.html")

# ================================================================
# Route for login
# ----------------------------------------------------------------

@app.route('/login')
def login():
    return render_template("login.html")
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
        tree = ET.parse('Database_Users.xml')  # Ensure the path to users.xml is correct
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

# ================================================================
# Route for test
# ----------------------------------------------------------------
        
@app.route('/test')
def test():
    return render_template("test.html")

# Start the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
