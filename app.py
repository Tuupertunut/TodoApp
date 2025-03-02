from flask import Flask, render_template, request, session, redirect, abort
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import secrets

app = Flask(__name__)
app.secret_key = os.environ["TODOAPP_SECRET_KEY"]


def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password_again"]

    if password_again != password:
        return render_template(
            "index.html", registration_result="Error: passwords do not match"
        )

    password_hash = generate_password_hash(password)

    try:
        db = sqlite3.connect("database.db")
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            [username, password_hash],
        )
        db.commit()
        db.close()
    except sqlite3.IntegrityError:
        return render_template(
            "index.html", registration_result="Error: username already taken"
        )
    except Exception as error:
        return render_template(
            "index.html", registration_result="Error: " + repr(error)
        )

    return render_template(
        "index.html", registration_result="Successfully registered user " + username
    )


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    try:
        db = sqlite3.connect("database.db")
        row = db.execute(
            "SELECT id, password_hash FROM users WHERE username = ?",
            [username],
        ).fetchone()
        db.close()
    except Exception as error:
        return render_template("index.html", login_result="Error: " + repr(error))

    if row is None:
        return render_template("index.html", login_result="Error: username not found")

    [user_id, password_hash] = row

    if not check_password_hash(password_hash, password):
        return render_template("index.html", login_result="Error: incorrect password")

    session["user_id"] = user_id
    session["username"] = username
    session["csrf_token"] = secrets.token_hex(16)
    return redirect("/todos")


@app.route("/logout", methods=["POST"])
def logout():
    check_csrf()

    session.clear()
    return redirect("/")


@app.route("/todos")
def todos():
    username = session["username"]
    query = request.args.get("query")
    if query is None:
        query = ""

    try:
        db = sqlite3.connect("database.db")
        todoitems_rows = db.execute(
            """SELECT todoitems.id, item, todostates.id, state FROM todoitems
            JOIN todostates ON todoitems.todostate_id = todostates.id
            JOIN users ON todoitems.user_id = users.id
            WHERE username = ? AND item LIKE ?""",
            [username, "%" + query + "%"],
        ).fetchall()
        todostates_rows = db.execute("SELECT id, state FROM todostates").fetchall()
        db.close()
    except Exception as error:
        return abort(repr(error))

    max_todostate_id = len(todostates_rows)

    return render_template(
        "todolist.html",
        username=username,
        query=query,
        todoitems=todoitems_rows,
        todostates=todostates_rows,
        max_todostate_id=max_todostate_id,
    )


@app.route("/todos/add", methods=["POST"])
def add_todo():
    check_csrf()
    user_id = session["user_id"]
    item = request.form["item"]

    try:
        db = sqlite3.connect("database.db")
        # The default todostate is the one with id 1
        db.execute(
            "INSERT INTO todoitems (item, user_id, todostate_id) VALUES (?, ?, 1)",
            [item, user_id],
        )
        db.commit()
        db.close()
    except Exception as error:
        return abort(repr(error))

    return redirect("/todos")


@app.route("/todos/evolve/<int:todo_id>", methods=["POST"])
def evolve_todo(todo_id):
    check_csrf()
    user_id = session["user_id"]

    try:
        db = sqlite3.connect("database.db")
        db.execute(
            "UPDATE todoitems SET todostate_id = todostate_id + 1 WHERE id = ? AND user_id = ?",
            [todo_id, user_id],
        )
        db.commit()
        db.close()
    except Exception as error:
        return abort(repr(error))

    return redirect("/todos")


@app.route("/todos/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    check_csrf()
    user_id = session["user_id"]

    try:
        db = sqlite3.connect("database.db")
        db.execute(
            "DELETE FROM todoitems WHERE id = ? AND user_id = ?",
            [todo_id, user_id],
        )
        db.commit()
        db.close()
    except Exception as error:
        return abort(repr(error))

    return redirect("/todos")


@app.route("/todos/edit/<int:todo_id>", methods=["POST"])
def edit_todo(todo_id):
    check_csrf()
    user_id = session["user_id"]
    new_item = request.form["item"]

    try:
        db = sqlite3.connect("database.db")
        db.execute(
            "UPDATE todoitems SET item = ? WHERE id = ? AND user_id = ?",
            [new_item, todo_id, user_id],
        )
        db.commit()
        db.close()
    except Exception as error:
        return abort(repr(error))

    return redirect("/todos")
