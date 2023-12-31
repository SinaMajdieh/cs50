import sys
from flask import flash, redirect, render_template, request, session
from queries import *
from database import *
from datetime import date
from helpers import apology, is_email_valid, is_age_valid, is_cap_valid, right_now
from werkzeug.security import check_password_hash, generate_password_hash
import shared

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
        users = shared.db.getUserByUsername(request.form.get("username"))
        
        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(users[0]["hash"], request.form.get("password")):
            return apology("invalid username or password")
        
             
        # Remember which user has logged in
        session["user_id"] = users[0]["id"]
        session["user_country"] = shared.db.getCountryByUserId(session["user_id"])[0]
        
        # Flash the user for logging in
        flash("Welcome, " + request.form.get("username"))
        
        # redirect user to homepage
        return redirect("/")
    
    # User reached route via GET    
    else:
        return render_template("login.html")


def validate_registration_form(form):
    """Ensuring registration form is valid"""
    # Ensure user provided all the required information
    for key in form:
        if not form[key]:
            return "Must provide all the information"
    
    # Ensure user provided valid email, age, and country
    if not shared.countries.is_valid(form["country"]):
        return "Country field was not filled correctly"
    if not is_email_valid(form["email"]):
        return "Your email pattern is not correct"
    if not is_age_valid(form["age"]):
        return "you are under 18 or age field was not filled correctly"
    
    # Ensuring the user name was not taken
    if len(shared.db.getUserByUsername(form["username"])) != 0:
        return "username was taken"
    
    # Ensureing that email does not exist
    if len(shared.db.getDescriptionByEmail(form["email"])) != 0:
        return "there is already an account associated with this email"
    
    # Ensuring the confirmation mathces the password
    if form["confirmation"] != form["password"]:
        return "confirmation does not match the provided password"

    return ""


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

        # Ensuring the form is valid
        validation = validate_registration_form(form)
        if validation != "":
            return apology(validation)
        
        # Hadh the user's password
        password_hash = generate_password_hash(form["password"])
        
        # Query database to insert the new user and their description
        shared.db.insertUser(form["username"], password_hash)
        form["user_id"] = shared.db.getUserByUsername(form["username"])[0]["id"]
        shared.db.insertDescription(form)
        
        # Flash the user for registering
        flash("Registration successful, you may now log in.")
        
        # Redirect the user to home page
        return redirect("/")
    # User reached via GET
    else:
        return render_template("register.html", countries=shared.countries.countries)