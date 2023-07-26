import sys
from flask import flash, redirect, render_template, request, session
from queries import *
from database import *
from datetime import date
from helpers import apology, is_email_valid, is_age_valid, is_cap_valid, right_now
from werkzeug.security import check_password_hash, generate_password_hash
import shared
from enrolRouteHelper import user_is_enroled_in_event, user_is_event_creator, destroy_event


def handlemyevents():
    events = shared.db.getEventByUserId(session["user_id"], shared.stats.lookup_key("open"))
    return render_template("myevents.html", events=events, exists=bool(events))


def validate_add_event(form):
    """Validating event proprties"""
    
    # Ensure user provided all the fields in the form
    for key in form:
        if not form[key]:
            return "Make sure to fill out all the fields"
        
    # Ensure tags and cap are valid
    if not shared.tags.are_valid([tag_id for tag_id in form["tags"].split(';') if tag_id != ""]):
        return "There is something wrong with tags"
    if not is_cap_valid:
        return "There is something wrong with caps"
    
    return ""

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
        "state": shared.stats.lookup_key("open"),
        "timestamp" : right_now(),
        "tags": request.form.get("tags"),  
    }
       
    # Ensuring form is valid
    validation = validate_add_event(form)
    if validation != "":
        return apology(validation)
    
    # Query database to insert new event
    shared.db.insertEvent(form)
    
    # Create ebtry form for the creatoe
    event_id = shared.db.lastId("events")[0]["seq"]
    entry_form = {
        "user_id": session["user_id"],
        "event_id": event_id,
        "timestamp": right_now(),
    }
    
    # Query database to insert new entry
    shared.db.insertEntry(entry_form)
    
    # Redirect to myevents via POST
    return redirect("/myevents")


def handle_addevent_get():
    """"
    User has reached via GET
    Submittion from should be displayed to user
    """
    return render_template("add_event_form.html", tags=shared.tags.tags)


# def delete_event(id):
#     # Changing the state of the event to deleted
#     delete_state = shared.stats.lookup_key("deleted")
#     shared.db.changeEventState(id, state_id=delete_state)
    
#     # Flash the user
#     flash("event deleted")
    
#     # Redirect to the myevents page
#     return redirect("/myevents") 


def validate_edited_form(form, event):
    # Ensure user provided all the required fields
    for key in form:
        if not form[key]:
            return apology("Make sure to fill out all the fields")
        
    # Ensure tags and cap are valid
    if not shared.tags.are_valid([tag_id for tag_id in form["tags"].split(';') if tag_id != ""]):
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
    if len(shared.db.eventByIdUserId(id, session["user_id"], shared.stats.lookup_key("open"))) == 0:
        return apology("You dont have access to this event or it does not exist")
   
    # event was created by user
    else:
        event = shared.db.getEventById(id, shared.stats.lookup_key("open"))[0]
        
        # User reached via POST
        if request.method == "POST":
            
            # Extracting information sent via POST form
            form = {
                "title": request.form.get("title"),
                "details": request.form.get("details"),
                "date": request.form.get("date"),
                "cap": request.form.get("cap"),
                "state": shared.stats.lookup_key("open"),
                "tags": request.form.get("tags"),  
            }       
            
            # Validating form
            form = validate_edited_form(form, event)
            
            # Querry update for the event
            result = shared.db.updateEventCustomById(id, form)
            
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
            return render_template("edit_event_form.html", form=form, tags=shared.tags.tags)
 
 
def handle_events():
    """
    Habdle events
    Show user all events they are a part of
    """
    events = shared.db.getEventsUserEnroled(session["user_id"], shared.stats.lookup_key("open"), joinedCountry=True)
    
    # Render the results
    return render_template("events.html", events=events)
 

def handle_event(id):
    """Handle event"""
    # User hasnt logged in 
    if "user_id" not in session:
        visitor_id = -1
    else:
        visitor_id = session["user_id"]

    # Query for event 
    event = shared.db.getEventById(id, shared.stats.lookup_key("open"), joinedCountries=True)
    
    # Ensure event exists
    if len(event) == 0:
        return apology("event was not found")
    
    # user is creator
    creator = user_is_event_creator(id)
    enroled = True

    # user is enroled
    if not creator:
      enroled = user_is_enroled_in_event(id)
    
    
    # Query for entries
    entries = []
    if enroled:
        entries = shared.db.getEntriesByEventIdJoinedUsers(visitor_id, id, shared.stats.lookup_key("open"))
    
    # Render the results
    return render_template("event.html", event=event[0], entries=entries, user_id=visitor_id, enroled=enroled, creator=creator)


def handle_delete_event(id):
    """Handling delete request from user"""
    # Ensure event exists
    event = shared.db.getEventById(id, shared.stats.lookup_key("open"))
    if len(event) == 0:
        return apology("event does not exist")
    
    # Ensure user is the creator
    if not user_is_event_creator(id):
        return apology("You cannot perform this act on this event")
    
    # destrying the event
    destroy_event(id)
    
    # Flash the user
    flash("event deleted")
    
    # Redirect to myevents
    return redirect("/myevents")
    