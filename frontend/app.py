from flask import Flask, render_template

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template("index.html")

# Start the Flask application
if __name__ == "__main__":
    # Running on host '0.0.0.0' to be accessible from outside the container
    app.run(host="0.0.0.0", port=8000)
