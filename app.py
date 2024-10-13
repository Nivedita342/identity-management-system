from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection function
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',          # Update this if you use a different username
        password='nivedita',  # Your password
        database='identity_management_db'  # Your database name
    )

# Home route
@app.route('/')
def home():
    return render_template('register.html')

# User registration route
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        connection.commit()
        return redirect(url_for('users'))
    except Error as e:
        print("Error while connecting to MySQL", e)
        return "Error occurred during registration."
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# Users list route
@app.route('/users')
def users():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        user_list = cursor.fetchall()
        return render_template('users.html', users=user_list)
    except Error as e:
        print("Error while connecting to MySQL", e)
        return "Error occurred while fetching users."
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    app.run(debug=True)
