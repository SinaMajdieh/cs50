import sys
from flask import flash, redirect, render_template, request, session
from queries import *
from database import *
from datetime import date
from helpers import apology, is_email_valid, is_age_valid, is_cap_valid, right_now
from werkzeug.security import check_password_hash, generate_password_hash
import shared


def user_is_event_creator(event_id) -> bool:
    creator_form = {
        "creator_id": session["user_id"],
        "id": event_id,
    }
    rows = shared.db.getEventsCustom(creator_form)
    if len(rows) != 0:
        return True
    return False


def user_is_enroled_in_event(event_id) -> bool:
    enrol_form = {
        "user_id": session["user_id"],
        "event_id": event_id,
    }
    rows = shared.db.getEntryCustome(enrol_form)
    if len(rows) != 0:
        return True
    return False


def handle_enrol(id):
    """Handle enroling"""
    # Finding the event
    event = shared.db.getEventById(id, shared.stats.lookup_key("open"))
   
    # Ensure event exists
    if len(event) == 0:
        return apology("the event was not found")
    
    # Ensure user hasn't enrolled already
    if user_is_enroled_in_event(id):
        return apology("You have already enrolled in this event")

    # Ensure event hasn't reached it's limit
    if event[0]["enroled"] == event[0]["cap"]:
        return apology("this event has reached it's limit")    
    
    # Ensure user is enroling for an event in their country
    if  event[0]["country_id"] != session["user_country"]["id"]:
        return apology("this event is not in your country")
    
    # Enrol the user
    form = {
        "user_id": session["user_id"],
        "event_id": id,
    }
    update_enroled = {
        "enroled": event[0]["enroled"]+1
    }
    shared.db.updateEventCustomById(id, update_enroled)
    form["timestamp"] = right_now()
    shared.db.insertEntry(form)
    # Flash the user
    flash("successfully enrolled")
    # Redirect to events
    return redirect("/events")


def destroy_event(id):
    """destroy event and all entries to the event"""
    # Setting event state to deleted
    shared.db.changeEventState(id, shared.stats.lookup_key("deleted"))
    
    # Deleting all entries to the event
    shared.db.deleteEventEntry(id)
    
    
def change_event_owner(id):
    """Chnage events ownership to the next person who joined the event"""
    # Finding the next person who enroled
    form = {
        "event_id": id,
    }
    new_owner_id = shared.db.getEntryCustome(form, sorted=True)[0]["user_id"]
    
    # updating the creator to the next person
    ownership = {
        "creator_id": new_owner_id,
    }
    shared.db.updateEventCustomById(id, ownership)

def handle_leave(id):
    "User wants to leave the the event"
    # Ensure users event exists
    event = shared.db.getEventById(id, shared.stats.lookup_key("open"))
    if len(event) == 0:
        return apology("event does not exists")
    
    # Ensure user is enrolled in the event
    if not user_is_enroled_in_event(id):
        return apology("you are not enrolled in this event")
    
    # user is the last person in the event
    if event[0]["enroled"] == 1:
        destroy_event(id)
        # delete user from entry
        shared.db.deleteEntryByUserByEvent(session["user_id"], id)
    else:
        # User is creator
        if user_is_event_creator(id):
            # delete user from entry
            shared.db.deleteEntryByUserByEvent(session["user_id"], id)
            change_event_owner(id)
            
        else:
            # delete user from entry
            shared.db.deleteEntryByUserByEvent(session["user_id"], id)    
        
        # Updating the enroled attribute
        form = {
                "enroled": event[0]["enroled"]-1,
            }
        shared.db.updateEventCustomById(id, form)
   
    # Flash the user
    flash("you left the event")
    
    # Redirect to events
    return redirect("/events")