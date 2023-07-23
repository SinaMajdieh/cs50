# Handler functions for routes
from flask import flash, redirect, render_template, request, session
from queries import *
from database import *
from datetime import date
from helpers import apology, is_country_valid, is_email_valid, is_age_valid, are_tags_valid, is_cap_valid, right_now
from werkzeug.security import check_password_hash, generate_password_hash


sqlite_path = "adventures_with_strangers.db"


def initial_database():
    """Using the database interface to open the database
    load basic data from database into memmory"""
    global db, countries, tags
    db = Sqlitedb(sqlite_path)
    countries = db.load_countries()
    tags = db.load_tags()


# Index handler(s)
def handleindex():
    """Handling the index request"""
    
    # Check session is available (user is logged in)
    if "user_id" in session:
        return render_template("index.html", countries=countries, defaultcountry=session["user_country"], date=date.today())
    # User has not logged in
    else:
        return render_template("index.html", countries=countries, defaultcountry={"id" : 0, "name" : "Global"}, date=date.today())


# login, log out, register handler(s)
def handlelogin():
    """Handling the login request"""
    
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
        users = db.getUserByUsername(request.form.get("username"))
        
        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(users[0]["hash"], request.form.get("password")):
            return apology("invalid username or password")
        
             
        # Remember which user has logged in
        session["user_id"] = users[0]["id"]
        session["user_country"] = db.getCountryByUserId(session["user_id"])[0]
        
        # Flash the user for logging in
        flash("Welcome, " + request.form.get("username"))
        
        # redirect user to homepage
        return redirect("/")
    
    # User reached route via GET    
    else:
        return render_template("login.html")


def handleregister():
    """Handling the register request"""
    
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
        
        # Ensure user provided valid email, age, and country
        if not is_country_valid(form["country"], countries):
            return apology("Country field was not filled correctly")
        if not is_email_valid(form["email"]):
            return apology("Your email pattern is not correct")
        if not is_age_valid(form["age"]):
            return apology("you are under 18 or age field was not filled correctly")
        
        # Ensuring the user name was not taken
        if len(db.getUserByUsername(form["username"])) != 0:
            return apology("username was taken")
        
        # Ensureing that email does not exist
        if len(db.getDescriptionByEmail(form["email"])) != 0:
            return apology("there is already an account associated with this email")
        
        # Ensuring the confirmation mathces the password
        if form["confirmation"] != form["password"]:
            return apology("confirmation does not match the provided password")
        
        # Hadh the user's password
        password_hash = generate_password_hash(form["password"])
        
        # Query database to insert the new user and their description
        db.insertUser(form["username"], password_hash)
        form["user_id"] = db.getUserByUsername(form["username"])[0]["id"]
        db.insertDescription(form)
        
        # Flash the user for registering
        flash("Registration successful, you may now log in.")
        
        # Redirect the user to home page
        return redirect("/")
    # User reached via GET
    else:
        return render_template("register.html", countries=countries)
    

# events handler(s)
def handlemyevents():
    events = db.getEventByUserId(session["user_id"])
    return render_template("myevents.html", events=events, exists=bool(events))


def handle_addevent_post():
    """
    User has reached via POST
    New event should be validated and evntually added
    """

    # Extraxt field values from form
    form = {
        "title": request.form.get("title"),
        "country_id": session["user_country"]["id"],
        "creator_id": session["user_id"],
        "details": request.form.get("details"),
        "date": request.form.get("date"),
        "cap": request.form.get("cap"),
        "enroled": 1,
        "state": "open",
        "timestamp" : right_now(),
        "tags": request.form.get("tags"),
        
    }
       
    # Ensure user provided all the fields in the form
    for key in form:
        if not form[key]:
            return apology("Make sure to fill out all the fields")
        
    # Ensure tags and cap are valid
    if not are_tags_valid([tag_id for tag_id in form["tags"].split(';') if tag_id != ""], tags):
        return apology("There is something wrong with tags")
    if not is_cap_valid:
        return apology("There is something wrong with caps")
    
    # Query database to insert new event
    db.insertEvent(form)
    
    # Create ebtry form for the creatoe
    event_id = db.lastId("events")[0]["seq"]
    entry_form = {
        "user_id": session["user_id"],
        "event_id": event_id,
        "timestamp": right_now(),
    }
    
    # Query database to insert new entry
    db.insertEntry(entry_form)
    
    # Redirect to myevents via POST
    return redirect("/myevents")

def handle_addevent_get():
    """"
    User has reached via GET
    Submittion from should be displayed to user
    """
    return render_template("add_event_form.html", tags=tags)
        