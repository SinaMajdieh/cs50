import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

ALL_BDS_QUERY = "SELECT * FROM birthdays;"
ADD_BD_QUERY = "INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?);"


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        try:
            month = int(month)
            day = int(day)
        except ValueError:
            return redirect("/")
        
        if not name or not month or not day:
            return redirect("/")

        
        db.execute(ADD_BD_QUERY, name, month, day)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        bds = db.execute(ALL_BDS_QUERY)

        return render_template("index.html",bds=bds)


