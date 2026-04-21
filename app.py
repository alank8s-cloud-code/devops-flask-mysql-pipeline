import os
import time

from dotenv import load_dotenv
from flask import Flask, request, render_template
import mysql.connector
from mysql.connector import Error
from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "dev-secret-key-change-this"
)
bcrypt = Bcrypt(app)

# Database configuration
DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST"),
    "port": int(os.environ.get("MYSQL_PORT", "3306")),
    "user": os.environ.get("MYSQL_USER"),
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": os.environ.get("MYSQL_DATABASE"),
}


def get_db_connection():
    """Create and return a MySQL connection."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


def init_db():
    """Initialize database with users table."""
    for _ in range(10):
        connection = get_db_connection()

        if connection:
            try:
                cursor = connection.cursor()

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(100) UNIQUE,
                        email VARCHAR(100) UNIQUE,
                        password_hash VARCHAR(255)
                    )
                    """
                )

                connection.commit()
                print("USERS table created!")

                cursor.close()
                connection.close()
                return

            except Exception as err:  # noqa: BLE001
                print("Retry DB init...", err)

        else:
            print("Waiting for MySQL...")

        time.sleep(3)

    print("Failed to initialize DB after retries")


# 🔥 IMPORTANT: Run DB init once (safe for Gunicorn)
init_db()


@app.route("/")
def home():
    """Render home page."""
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration."""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        password_hash = bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    (
                        "INSERT INTO users "
                        "(username, email, password_hash) "
                        "VALUES (%s, %s, %s)"
                    ),
                    (username, email, password_hash),
                )
                connection.commit()
                return "User Registered Successfully"

            except Exception as err:  # noqa: BLE001
                return f"Error: {err}"

            finally:
                cursor.close()
                connection.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(
                    "SELECT * FROM users WHERE username=%s",
                    (username,),
                )
                user = cursor.fetchone()

                if user and bcrypt.check_password_hash(
                    user["password_hash"], password
                ):
                    return "Login Success"

                return "Invalid Credentials"

            finally:
                cursor.close()
                connection.close()

        return "DB Error"

    return render_template("login.html")


if __name__ == "__main__":
    app.run(port=5000)
