from flask import Flask, request, redirect, render_template_string
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
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login Form</title>
        </head>
        <body>
            <h2>Login Form</h2>
            <form action="/login" method="post">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username" required><br><br>
                
                <label for="password">Password:</label><br>
                <input type="password" id="password" name="password" required><br><br>
                
                <input type="submit" value="Login">
            </form>
        </body>
        </html>
    '''

# Route to handle login logic
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Validate username and password against the database
    user = validate_user(username, password)
    
    if user:
        # If user exists in the database
        return '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Login Success</title>
            </head>
            <body>
                <h2>Logged in successfully!</h2>
            </body>
            </html>
        '''
    else:
        # If the username or password is incorrect
        return '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Login Failed</title>
            </head>
            <body>
                <h2>Wrong username or password. Please try again.</h2>
                <form action="/login" method="post">
                    <label for="username">Username:</label><br>
                    <input type="text" id="username" name="username" required><br><br>
                    
                    <label for="password">Password:</label><br>
                    <input type="password" id="password" name="password" required><br><br>
                    
                    <input type="submit" value="Login">
                </form>
            </body>
            </html>
        '''

if __name__ == "__main__":
    app.run(debug=True)
