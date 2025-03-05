
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helper import login_required, error


# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    tasks = db.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY DEADLINE ASC", session["user_id"])
    if request.method == "POST":
        taskid = request.form.get("task_id")
        if "delete" in request.form: # delete button is clicked
            db.execute("DELETE FROM tasks WHERE task_id = ?", taskid)
            tasks = db.execute("SELECT * FROM tasks WHERE user_id = ?", session["user_id"])
            return render_template("menu.html", tasks=tasks)
        else: #approve button is clicked
            tasks = db.execute("SELECT * FROM tasks WHERE task_id = ? ORDER BY DEADLINE ASC", taskid)
            current_date = datetime.now()
            formatted_date = current_date.strftime('%m-%d-%Y') # y m d
            db.execute("INSERT INTO history (user_id, TITLE, DESCRIPTION, DEADLINE, FINISHED) VALUES (?,?,?,?,?)", session["user_id"], tasks[0]["TITLE"], tasks[0]["DESCRIPTION"], tasks[0]["DEADLINE"], formatted_date)
            db.execute("DELETE FROM tasks WHERE task_id = ?", taskid)
            tasks = db.execute("SELECT * FROM tasks WHERE user_id = ?", session["user_id"])

            return render_template("menu.html", tasks=tasks)
    else:
        return render_template("menu.html", tasks=tasks)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")


        if not request.form.get("username"):
            return error("Must provide username", 400)

        if not password:
            return error("Must provide password", 400)

        if not confirmation:
            return error("Must provide a confirmation for the password", 400)

        if password != confirmation:
            return error("Password does not match the confirmation", 400)

        rows = db.execute(
                "SELECT * FROM users WHERE username = ?", request.form.get("username")
            )

        if len(rows) == 1:
            return error("This username is already taken", 400)

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (USERNAME, PASSWORD) VALUES (?,?)", request.form.get("username"), hash)

        rows = db.execute(
                "SELECT * FROM users WHERE username = ?", request.form.get("username")
            )
        session["user_id"] = rows[0]["user_id"]
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("username"):
            return error("Must provide username", 400)
        if not request.form.get("password"):
            return error("Must provide a password", 400)
        rows = db.execute(
                "SELECT * FROM users WHERE username = ?", request.form.get("username")
                )
        if len(rows) != 1 or not check_password_hash(rows[0]["PASSWORD"], request.form.get("password")):
             return error("invalid username and/or password", 403)
        session["user_id"] = rows[0]["user_id"]
        tasks = db.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY DEADLINE ASC", session["user_id"])
        return render_template("menu.html", tasks=tasks)



    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()


    # Redirect user to login form
    return redirect("/login")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        deadline = request.form.get("deadline")
        deadline = datetime.strptime(deadline, "%Y-%m-%d")
        deadline = deadline.strftime('%Y-%m-%d')
        if not request.form.get("title"):
            return error("Must provide a title", 400)
        if not deadline:
            return error("Must provide a deadline", 400)
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y-%m-%d')

        db.execute("INSERT INTO tasks (user_id, TITLE, DESCRIPTION, DEADLINE, CREATED) VALUES (?,?,?,?,?)", session["user_id"], request.form.get("title"), request.form.get("description"),deadline, formatted_date)

        return redirect(url_for("index"))
    else:
        return render_template("add.html")

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    tasks = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY FINISHED DESC", session["user_id"])
    if request.method == "POST":
        history_id = request.form.get("history")
        if history_id:
            print(history_id)
            db.execute("DELETE FROM history WHERE history_id = ?", history_id)
            tasks = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY FINISHED DESC", session["user_id"])
            return render_template("history.html",tasks=tasks)
    else:
        return render_template("history.html", tasks=tasks)


