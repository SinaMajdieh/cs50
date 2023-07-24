import sys
from flask import flash, redirect, render_template, request, session
from queries import *
from database import *
from datetime import date
from helpers import apology, is_email_valid, is_age_valid, is_cap_valid, right_now
from werkzeug.security import check_password_hash, generate_password_hash


sqlite_path = "adventures_with_strangers.db"

class Stats:
    def __init__(self, value):
        self.stats = value
    def lookup_key(self, msg):
        """Finds the id of a certain stat"""
        for stat in self.stats:
            if stat["text"] == msg:
                return stat["id"]
        # State message does not exist in the stats
        return -1
    
class Tags:
    def __init__(self, value):
        self.tags = value
    def are_valid(self, ids):
        """Ensure tags are valid"""
        # Ensure ids are integers
        for i in range(len(ids)):
            try:
                ids[i] = int(ids[i])
            except ValueError:
                return False
        
        # Ensre all ids are valid
        found = 0
        for id in ids:
            for tag in self.tags:
                if id == tag["id"]:
                    found += 1
        
        
        # Ensure all ids were found in tags
        if found == len(ids):
            return True
        else:
            return False
        

class Countries:
    def __init__(self, value):
        self.countries = value
        
    def lookup(self, id):
        """looks up a country by its id"""
        try:
            id = int(id)
        except ValueError:
            return {}
        for country in self.countries:
            if country["id"] == id:
                return {
                    "id": id,
                    "name" : country["name"],
                }
        # State message does not exist in the stats
        return {}
    
    def is_valid(self, id):
        """Ensure country name exsist based on the list of dicts containing country id and name"""
        # Ensure country id is not 0
        if id == 0:
            return False
        # Ensure country id is an int
        try:
            id = int(id)
        except ValueError:
            return False
        for country in self.countries:
            if id == country["id"]:
                return True
        return False


def initial_database():
    """Using the database interface to open the database
    load basic data from database into memmory"""
    global db, countries, tags, stats
    db = Sqlitedb(sqlite_path)
    countries = Countries(db.load_countries())
    tags = Tags(db.load_tags())
    stats = Stats(db.load_stats())

# Handler functions for routes

def index_filter(form):
    """Replace default values if there is a filter"""
    # Extracting values from sent via get
    country = request.args.get("country")
    date = request.args.get("date")
    
    # user provided the filter with a country
    if country:
        # Ensure country is valid by looking for it
        result = countries.lookup(country)
        # Country was valid and it exists
        if result:
            # If country was set to global it means there are no filters for country
            if result["id"] == 0:
                if "country_id" in form:
                    del form["country_id"]
            # Set country id to the filtered country id
            else:
                form["country_id"] = result["id"]       
            # Set default country for the page content
            form["default_country"] = result
        # Country was not valid so setting default country to 0 which is global
        else:
            form["default_country"] = countries.lookup(0)
    # Date was provided as a filter
    if date:
        form["date"] = date
    return form

# Index handler(s)
def handleindex():
    """Handling the index request"""

    # Check session is available (user is logged in)
    if "user_id" in session:
        # apply filter
        form = {
            "country_id": session["user_country"]["id"],
            "date": date.today(),
            "default_country": session["user_country"],
            "state": stats.lookup_key("open"),
        }
        form = index_filter(form)
        events = db.getEventsUserEnroledAndAvailable(session["user_id"], form, desc=True, joinedCountries=True, joinedCreator=True)
        return render_template("index.html", countries=countries.countries, defaultcountry=form["default_country"], date=form["date"], events=events)
    # User has not logged in
    else:
        # country id 0 belong to global
        # apply filter
        form = {
            "date": date.today(),
            "default_country": countries.lookup(0),
            "state": stats.lookup_key("open"),
        }
        form = index_filter(form)
        events = db.getEventsCustom(form, desc=True, joinedCountries=True, joinedCreator=True)
        return render_template("index.html", countries=countries.countries, defaultcountry=form["default_country"], date=form["date"], events=events)


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
        if not countries.is_valid(form["country"]):
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
        return render_template("register.html", countries=countries.countries)
    

# events handler(s)
def handlemyevents():
    events = db.getEventByUserId(session["user_id"], stats.lookup_key("open"))
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
        "state": stats.lookup_key("open"),
        "timestamp" : right_now(),
        "tags": request.form.get("tags"),  
    }
       
    # Ensure user provided all the fields in the form
    for key in form:
        if not form[key]:
            return apology("Make sure to fill out all the fields")
        
    # Ensure tags and cap are valid
    if not tags.are_valid([tag_id for tag_id in form["tags"].split(';') if tag_id != ""]):
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
    return render_template("add_event_form.html", tags=tags.tags)


def delete_event(id):
    # Changing the state of the event to deleted
    delete_state = stats.lookup_key("deleted")
    db.changeEventState(id, state_id=delete_state)
    
    # Flash the user
    flash("event deleted")
    
    # Redirect to the myevents page
    return redirect("/myevents") 


def validate_edited_form(form, event):
    # Ensure user provided all the required fields
    for key in form:
        if not form[key]:
            return apology("Make sure to fill out all the fields")
        
    # Ensure tags and cap are valid
    if not tags.are_valid([tag_id for tag_id in form["tags"].split(';') if tag_id != ""]):
        return apology("There is something wrong with tags")
    if not is_cap_valid:
        return apology("There is something wrong with caps")
    
    # Ignore fields that havent been edited and keep track of how many changes
    ignored_keys = []
    for key in form:
        if str(form[key]) == str(event[key]):
            ignored_keys.append(key)
            
    # Ensure user has chnaged one attribute at least
    if len(ignored_keys) == len(form):
        return apology("You havent changed anything!")
    
    # Delete ignored keys from the form
    for key in ignored_keys:
        del form[key]
        
    return form


def handle_edit_event(id):
    """Handle user request to edit an event created by them"""
    
    # Ensure event was created by the user
    if len(db.eventByIdUserId(id, session["user_id"], stats.lookup_key("open"))) == 0:
        return apology("You dont have access to this event or it does not exist")
    # event was created by user
    else:
        event = db.getEventById(id, stats.lookup_key("open"))[0]
        # User reached via POST
        if request.method == "POST":
            # User wants to delete the event
            if request.form.get("delete") == "1":
                delete_event(id)
            # Extracting information sent via POST form
            form = {
                "title": request.form.get("title"),
                "details": request.form.get("details"),
                "date": request.form.get("date"),
                "cap": request.form.get("cap"),
                "state": stats.lookup_key("open"),
                "tags": request.form.get("tags"),  
            }       
            # Validating form
            form = validate_edited_form(form, event)
            
            # Querry update for the event
            result = db.updateEventCustomById(id, form)
            
            # Enssure update was successful
            if not result:
                return apology("There was something wrong while updating you event on the server")
            
            # Flash user
            flash("event updated")
            
            # Redirect to myevents page
            return redirect("/myevents")
        
        # User reached via GET
        else:
            # Finding the event attributes
            form = {
                "id": id,
                "title": event["title"],
                "details": event["details"],
                "date": event["date"],
                "cap": event["cap"],
                "tags": event["tags"],
            }
            
            # Prompt the user for edit information
            return render_template("edit_event_form.html", form=form, tags=tags.tags)
 
 
def handle_events():
    """
    Habdle events
    Show user all events they are a part of
    """
    events = db.getEventsUserEnroled(session["user_id"], stats.lookup_key("open"))
    
    # Render the results
    return render_template("events.html", events=events)
 
def is_user_event_creator(event_id) -> bool:
    creator_form = {
        "creator_id": session["user_id"],
        "id": event_id,
    }
    rows = db.getEventsCustom(creator_form)
    if len(rows) != 0:
        return True
    return False


def is_user_enroled_in_event(event_id) -> bool:
    enrol_form = {
        "user_id": session["user_id"],
        "event_id": event_id,
    }
    rows = db.getEntryCustome(enrol_form)
    if len(rows) != 0:
        return True
    return False
 

def handle_event(id):
    """Handle event"""
    # Query for event 
    event = db.getEventById(id, stats.lookup_key("open"), joinedCountries=True)
    print(event, file=sys.stderr)
    
    # Ensure event exists
    if len(event) == 0:
        return apology("event was not found")
    
    # user is creator
    creator = is_user_event_creator(id)
    enroled = True

    if not creator:
      enroled = is_user_enroled_in_event(id)
    # user is enroled
    
    
    # Query for entries
    entries = []
    if enroled:
        entries = db.getEntriesByEventIdJoinedUsers(session["user_id"], id, stats.lookup_key("open"))
    
    # Render the results
    return render_template("event.html", event=event[0], entries=entries, user_id=session["user_id"], enroled=enroled, creator=creator)
    
def handle_enrol(id):
    """Handle enroling"""
    # Finding the event
    event = db.getEventById(id, stats.lookup_key("open"))
    # Ensure event exists
    print(event, file=sys.stderr)
    if len(event) == 0:
        return apology("the event was not found")
    # Ensure user hasn't enrolled already
    # Create the search form
    form = {
        "user_id": session["user_id"],
        "event_id": id,
    }
    rows = db.getEntryCustome(form)
    if len(rows) != 0:
        return apology("You have already enrolled in this event")

    # Ensure event hasn't reached it's limit
    if event[0]["enroled"] == event[0]["cap"]:
        return apology("this event has reached it's limit")    
    
    # Ensure user is enroling for an event in their country
    if  event[0]["country_id"] != session["user_country"]["id"]:
        return apology("this event is not in your country")
    
    # Enrol the user
    update_enroled = {
        "enroled": event[0]["enroled"]+1
    }
    db.updateEventCustomById(id, update_enroled)
    form["timestamp"] = right_now()
    db.insertEntry(form)
    # Flash the user
    flash("successfully enrolled")
    # Redirect to events
    return redirect("/events")
    