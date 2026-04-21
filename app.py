import os
from functools import wraps

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, session
)
import mysql.connector
from mysql.connector import Error
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "dev-secret-key-change-this"
)
bcrypt = Bcrypt(app)

# =========================
# DATABASE CONFIG (FIXED)
# =========================
DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("MYSQL_PORT", "3306")),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DATABASE", "mydb"),
}


def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def init_db():
    """Initialize database and create tables if they don't exist"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # USERS TABLE
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

            # TODOS TABLE (FIXED STRUCTURE)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS todos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    task VARCHAR(255) NOT NULL,
                    status ENUM('pending', 'completed')
                        DEFAULT 'pending',
                    user_id INT,
                    deleted BOOLEAN DEFAULT FALSE,
                    deleted_at TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # AUTH LOG TABLE (used in your code)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS auth_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    action VARCHAR(50),
                    ip_address VARCHAR(45),
                    username_attempted VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.commit()
            print("Database initialized successfully!")

        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            cursor.close()
            connection.close()


# =========================
# AUTH DECORATOR
# =========================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# =========================
# AUTH LOGGER
# =========================
def log_auth_action(action, user_id=None, username_attempted=None):
    """Insert a record into auth_logs"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            ip = request.remote_addr

            cursor.execute(
                """
                INSERT INTO auth_logs
                (user_id, action, ip_address, username_attempted)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, action, ip, username_attempted),
            )

            connection.commit()

        except Error as e:
            print(f"Error logging auth action: {e}")
        finally:
            cursor.close()
            connection.close()


# =========================
# AUTH ROUTES
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("All fields are required!", "error")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("register.html")

        password_hash = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO users (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    """,
                    (username, email, password_hash),
                )

                connection.commit()
                flash("Account created! Please log in.", "success")
                return redirect(url_for("login"))

            except Error as e:
                if "Duplicate entry" in str(e):
                    flash("Username or email already exists.", "error")
                else:
                    flash(f"Error creating account: {str(e)}", "error")

            finally:
                cursor.close()
                connection.close()

        flash("Database connection failed.", "error")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required!", "error")
            return render_template("login.html")

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)

                cursor.execute(
                    "SELECT * FROM users WHERE username = %s",
                    (username,),
                )
                user = cursor.fetchone()

                if user and bcrypt.check_password_hash(
                    user["password_hash"], password
                ):
                    session["user_id"] = user["id"]
                    session["username"] = user["username"]

                    log_auth_action(
                        "login",
                        user_id=user["id"],
                        username_attempted=username,
                    )

                    flash(f"Welcome back, {user['username']}!", "success")
                    return redirect(url_for("index"))

                log_auth_action("failed", username_attempted=username)
                flash("Invalid username or password.", "error")

            except Error as e:
                flash(f"Error during login: {str(e)}", "error")

            finally:
                cursor.close()
                connection.close()

        else:
            flash("Database connection failed.", "error")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    log_auth_action(
        "logout",
        user_id=session.get("user_id"),
        username_attempted=session.get("username"),
    )
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# =========================
# MAIN ROUTES
# =========================
@app.route("/")
@login_required
def index():
    connection = get_db_connection()
    todos = []

    if connection:
        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT * FROM todos
                WHERE user_id = %s AND deleted = FALSE
                ORDER BY created_at DESC
                """,
                (session["user_id"],),
            )

            todos = cursor.fetchall()

        except Error as e:
            flash(f"Error fetching todos: {str(e)}", "error")

        finally:
            cursor.close()
            connection.close()

    else:
        flash("Database connection failed", "error")

    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
@login_required
def add_todo():
    task = request.form.get("task")

    if not task:
        flash("Task cannot be empty!", "error")
        return redirect(url_for("index"))

    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO todos (task, user_id)
                VALUES (%s, %s)
                """,
                (task, session["user_id"]),
            )

            connection.commit()
            flash("Todo added successfully!", "success")

        except Error as e:
            flash(f"Error adding todo: {str(e)}", "error")

        finally:
            cursor.close()
            connection.close()

    return redirect(url_for("index"))


@app.route("/health")
def health():
    connection = get_db_connection()
    if connection:
        connection.close()
        return {"status": "healthy"}, 200
    return {"status": "unhealthy"}, 503


# =========================
# START APP the
# =========================
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
