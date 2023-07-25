from functools import wraps
from cs50 import SQL
from flask import Flask, redirect, session
from flask_session import Session
from indexRouteHelper import *
from loggingRoutesHelper import *
from eventsRouteHelper import *
from enrolRouteHelper import *
from shared import initial_database

initial_database()

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# User has to be logged in for the url
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


# Index route  declaration
# -------------------------------------------------------------------
@app.route("/")
def index():
    """Show the useres dashbord if they have logged in otherwise show them the guest page"""
    return handleindex()    
    

# Loggin route related declaration
# -------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    return handlelogin()
    
    
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
    
    return handleregister()


# Events route related declaration 
# -------------------------------------------------------------------
@app.route("/myevents")
@login_required
def myevents():
    """Show the user events created by them"""
    return handlemyevents()


@app.route("/createevent", methods=["GET", "POST"])
@login_required
def create_event():
    """Lets users create new events"""
    
    # user reached via POST
    if request.method == "POST":
        return handle_addevent_post()
    # user reached via get
    else:
        return handle_addevent_get()
    

@app.route("/myevents/<id>", methods=["GET", "POST"])
@login_required
def edit_event(id):
    """Let's users edit events created by them"""
    
    # Handle event eddinting
    return handle_edit_event(id)


@app.route("/events")
@login_required
def events():
    """Show user all the events they are a part of"""
    
    # Handle events
    return handle_events()


@app.route("/event/<id>")
def event(id):
    """Browse the event"""
    
    # Handle the event
    return handle_event(id)


@app.route("/delete/<id>")
@login_required
def delete_event(id):
    """Delete the event created by user"""
    
    # Handle deleting event
    return handle_delete_event(id)


# Enrolling related routes declaration
# -------------------------------------------------------------------
@app.route("/enrol/<id>")
@login_required
def enroll(id):
    """Let's user to enrol in events"""
    
    # Handle event enroling
    return handle_enrol(id)


@app.route("/leave/<id>")
@login_required
def leave_event(id):
    "Let's user leave the event"
    
    # Handle leaving event
    return handle_leave(id)

    