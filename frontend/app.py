from flask import Flask, render_template, request, redirect, url_for, flash
import random

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
            flash("Too low! Try again.", 'warning')
        elif guess > secret_number:
            flash("Too high! Try again.", 'warning')
        else:
            flash(f"Congratulations! You guessed the number {secret_number}.", 'success')
            # Reset the game after success
            return redirect(url_for('game'))

    return render_template("game.html", secret_number=secret_number)

# Start the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
