import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

app = Flask(__name__)

# MySQL configuration
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

db = SQLAlchemy(app)


@app.route("/")
def home():
    return "<h1>Welcome to SURAKSHA</h1>"


@app.route("/db-test")
def db_test():
    try:
        db.session.execute(text("SELECT 1"))
        return "<h1>MySQL Connection Successful!</h1>"

    except Exception as e:
        db.session.rollback()
        app.logger.exception("Database connection failed")
        return f"Database connection failed: {e}", 500

    finally:
        db.session.remove()


if __name__ == "__main__":
    app.run(debug=True)