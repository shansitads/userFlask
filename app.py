from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL
from helpers import login_required, hashit
import os
from functools import wraps


app = Flask(__name__)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_PERMANENTON_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = # argh can't show this...I still need to program the random hex key
# Session(app)


db = SQL("sqlite:///database.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html", name=session["user"]["name"], points=session["user"]["points"])
    else:
        pointsUp()
        return render_template("index.html", name=session["user"]["name"], points=session["user"]["points"])

def pointsUp():
    pointlist = db.execute("SELECT points FROM users WHERE username = :username;", username=session["user"]["username"])
    points=pointlist[0]['points']
    points += 0

    db.execute("UPDATE users SET points = :points WHERE username = :username;", points=points, username=session["user"]["username"])
    session["user"]["points"] = points


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        session.clear()
        return render_template("register.html")
    else:
        name = request.form.get("name")
        username = request.form.get("username")

        # Fields not filled
        if not username or not name or not request.form.get("password") or not request.form.get("repassword"):
            return render_template("apology.html", message="You must enter all fields.")

        # Password don't match
        if request.form.get("password")!=request.form.get("repassword"):
            return render_template("apology.html", message="Password does not match password confirmation.")

        # Query database for username to check if it already exists
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if len(rows) != 0:
            return render_template("apology.html", message="Username already exists. Please choose a different username.")

        # If registration succeeds, add user to database
        hashpass = hashit(password=request.form.get("password"), key=app.secret_key) # hash
        db.execute("INSERT INTO users (name, username, password, points) VALUES (:name, :username, :password, :points)", name=name, username=username, password=hashpass, points=0)

        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    # login page is fetched
    if request.method == "GET":
        return render_template("login.html")
    # data is posted from login page
    else:
        # Ensure username and password were entered
        if not request.form.get("userid") or not request.form.get("password"):
            return render_template("apology.html", message="You must enter all fields.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("userid"))

        # Ensure username exists and password is correct
        enteredPass = hashit(password=request.form.get('password'), key=app.secret_key) # hash

        if len(rows) != 1 or rows[0]['password'] != enteredPass:
            return render_template("apology.html", message="invalid username and/or password.")

        # Remember which user has logged in
        session["user"] = rows[0]

        # Redirect user to home page
        return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")
