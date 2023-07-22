from functools import wraps
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

from helpers import apology, is_country_valid, is_email_valid, is_age_valid
from queries import *

db = SQL("sqlite:///adventures_with_strangers.db")

countries = db.execute(SELECT_ALL_COUNTRIES)


app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    """Show the useres dashbord if they have logged in otherwise show them the guest page"""
    # Check session is available (user is logged in)
    if "user_id" in session:
        return render_template("index.html", countries=countries, defaultcountry=session["user_country"], date=date.today())
    # User has not logged in
    else:
        return render_template("index.html", countries=countries, defaultcountry={"id" : 0, "name" : "Global"}, date=date.today())
        
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    # Forget session
    session.clear()
    
    # User reached route via POST
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("Must provide password", 403)
        
        # Query database for username
        users = db.execute(GET_ALL_USERS_INFO_BY_USERNAME, request.form.get("username"))
        
        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(users[0]["hash"], request.form.get("password")):
            return apology("invalid username or password")
        
             
        # Remember which user has logged in
        session["user_id"] = users[0]["id"]
        session["user_country"] = db.execute(USER_ID_USER_COUNTRY, session["user_id"])[0]
        
        # redirect user to homepage
        return redirect("/")
    
    # User reached route via GET    
    else:
        return render_template("login.html")
    

@app.route("/logout")
@login_required
def logout():
    """Log user out"""
    
    # End the session
    session.clear()
    
    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user"""
    # Clear the last session
    session.clear()
    
    # User reached via POST
    if request.method == "POST":
        # Extracting the values submitted via POST
        form = {
            "username": request.form.get("username"),
            "name": request.form.get("name"),
            "lastname": request.form.get("lastname"),
            "country": request.form.get("country"),
            "age": request.form.get("age"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "confirmation": request.form.get("confirmation"),
        }

        # Ensure user provided all the required information
        for key in form:
            if not form[key]:
                return apology("Must provide all the information")
        
        # Ensuring the user name was not taken
        if len(db.execute(GET_ALL_USERS_INFO_BY_USERNAME, form["username"])) != 0:
            return apology("username was taken")
        
        # Ensuring the confirmation mathces the password
        if form["confirmation"] != form["password"]:
            return apology("confirmation does not match the provided password")
        
        # Ensure user provided valid email, age, and country
        if not is_country_valid(form["country"], countries):
            return apology("Country field was not filled correctly")
        if not is_email_valid(form["email"]):
            return apology("Your email pattern is not correct")
        if not is_age_valid(form["age"]):
            return apology("you are under 18 or age field was not filled correctly")
        
        # Hadh the user's password
        password_hash = generate_password_hash(form["password"])
        
        # Query database to insert the new user and their description
        db.execute(INSERT_NEW_USER, form["username"], password_hash)
        user_id = db.execute(GET_ALL_USERS_INFO_BY_USERNAME, form["username"])[0]["id"]
        db.execute(INSERT_DESCRIPTION, form["name"], form["lastname"], form["email"], form["age"] , user_id, form["country"])
        
        # Redirect the user to login page
        return redirect("/login")
    # User reached via GET
    else:
        return render_template("register.html", countries=countries)