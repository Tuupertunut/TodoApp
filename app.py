from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]

    if password_again != password:
        return "Error: passwords do not match"

    password_hash = generate_password_hash(password)

    db = sqlite3.connect("database.db")
    db.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        [username, password_hash],
    )
    db.commit()
    db.close()

    return "registered user " + username + " " + password
