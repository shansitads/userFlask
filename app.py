from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from cs50 import SQL

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_PERMANENTON_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///users.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
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
        hashpass = hash(request.form.get("password"))
        db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)", name=name, username=username, password=hashpass)
        return redirect("/")

@app.route("/login", methods=["GET, POST"])
def login():
    # login page is fetched
    if request.method == "GET":
        return render_template("login.html")

    # data is posted from login page
    else:
        # Ensure username was submitted
        if not request.form.get("username") or request.form.get("password"):
            return render_template("apology.html", message="You must enter all fields.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apology.html", message="invalid username and/or password.")

        # Redirect user to home page
        return redirect("/")
