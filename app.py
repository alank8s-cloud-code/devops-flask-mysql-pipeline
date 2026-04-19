from dotenv import load_dotenv
load_dotenv()

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, session
)
import mysql.connector
from mysql.connector import Error
import os
from flask_bcrypt import Bcrypt
from functools import wraps
import time

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this')
bcrypt = Bcrypt(app)

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('MYSQL_HOST'),
    'port': int(os.environ.get('MYSQL_PORT', '3306')),
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'database': os.environ.get('MYSQL_DATABASE')
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# ✅ FIXED INIT (RETRY + FORCE TABLE CREATE)
def init_db():
    for i in range(10):
        connection = get_db_connection()

        if connection:
            try:
                cursor = connection.cursor()

                # USERS TABLE
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(100) UNIQUE,
                        email VARCHAR(100) UNIQUE,
                        password_hash VARCHAR(255)
                    )
                """)

                connection.commit()
                print("✅ USERS table created!")

                cursor.close()
                connection.close()
                return

            except Exception as e:
                print("Retry DB init...", e)

        else:
            print("⏳ Waiting for MySQL...")

        time.sleep(3)

    print("❌ Failed to initialize DB after retries")


# SIMPLE ROUTES (ONLY REGISTER + LOGIN WORKING)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, password_hash)
                )
                connection.commit()
                return "User Registered Successfully ✅"

            except Exception as e:
                return f"Error: {e}"

            finally:
                cursor.close()
                connection.close()

    return "Register Page"


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()

            if user and bcrypt.check_password_hash(user['password_hash'], password):
                return "Login Success 🚀"
            else:
                return "Invalid Credentials ❌"

        finally:
            cursor.close()
            connection.close()

    return "DB Error"


@app.route('/')
def home():
    return "Flask + MySQL Working 🚀"


if __name__ == '__main__':
    init_db()
    app.run(port=5000)
