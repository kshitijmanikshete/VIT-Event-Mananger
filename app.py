from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to insert data into the SQLite database (used for signup or initial insert)
def insert_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Function to check if username and password exist in the database
def validate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user  # Will return the row if the user exists, None otherwise

# Route for displaying the login form
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = validate_user(username, password)
    if user:
        return "Login successful!"
    else:
        return "Invalid username or password", 401

if __name__ == '__main__':
    app.run(debug=True)