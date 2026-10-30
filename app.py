import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "suraksha-local-development-key")

db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "")
db_host = os.getenv("DB_HOST", "127.0.0.1")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME", "suraksha_db")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{db_user}:{db_password}"
    f"@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["REMEMBER_COOKIE_HTTPONLY"] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(30), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="citizen")
    volunteer_id = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("volunteer_id", name="uq_users_volunteer_id"),)


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Enter your email address and password to continue.", "error")
        else:
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                session.clear()
                session["user_id"] = user.id
                session["user_name"] = user.name
                session["user_role"] = user.role
                session.permanent = request.form.get("remember") == "on"
                return redirect(url_for("dashboard"))
            flash("The email or password you entered is incorrect.", "error")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "citizen")
        volunteer_id = request.form.get("volunteer_id", "").strip() if role == "volunteer" else None

        if role not in {"citizen", "volunteer"}:
            flash("Choose Citizen or Volunteer to create an account.", "error")
        elif not name or not email or not phone or not password:
            flash("Fill in all required fields to continue.", "error")
        elif len(password) < 8:
            flash("Use a password with at least 8 characters.", "error")
        elif password != confirm_password:
            flash("The passwords do not match.", "error")
        elif role == "volunteer" and not volunteer_id:
            flash("Enter your volunteer ID to register as a volunteer.", "error")
        elif User.query.filter_by(email=email).first():
            flash("An account with this email already exists. Please sign in.", "error")
        elif volunteer_id and User.query.filter_by(volunteer_id=volunteer_id).first():
            flash("This volunteer ID is already linked to an account.", "error")
        else:
            user = User(
                name=name,
                email=email,
                phone=phone,
                password_hash=generate_password_hash(password),
                role=role,
                volunteer_id=volunteer_id,
            )
            db.session.add(user)
            db.session.commit()
            flash("Your account was created. You can sign in now.", "success")
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template(
        "dashboard.html",
        name=session.get("user_name", "there"),
        role=session.get("user_role", "citizen"),
    )


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/db-test")
def db_test():
    try:
        db.session.execute(text("SELECT 1"))
        return "<h1>MySQL Connection Successful!</h1>"
    except Exception:
        db.session.rollback()
        app.logger.exception("Database connection failed")
        return "Database connection failed. Check your MySQL service and .env settings.", 500
    finally:
        db.session.remove()


if __name__ == "__main__":
    app.run(debug=True)
