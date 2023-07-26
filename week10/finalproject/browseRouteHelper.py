import sys
from flask import flash, redirect, render_template, request, session
from queries import *
from database import *
from datetime import date
from helpers import apology, is_email_valid, is_age_valid, is_cap_valid, right_now
from werkzeug.security import check_password_hash, generate_password_hash
from indexRouteHelper import index_filter
import shared


def handle_browse(name):
    """Handles browse request"""
    # Ensure name is valid
    tag = shared.tags.lookup_title(name)
    if tag == None:
        return apology("this category does not exists")
    if "user_id" in session:
        form = {
            "country_id": session["user_country"]["id"],
            "date": date.today(),
            "default_country": session["user_country"],
            "state": shared.stats.lookup_key("open"),
        }
    # User has not logged in
    else:
        # country id 0 belong to global
        form = {
            "date": date.today(),
            "default_country": shared.countries.lookup(0),
            "state": shared.stats.lookup_key("open"),
        }
    
    # Aplly filter
    form = index_filter(form)
    events = shared.db.getEventsCustom(form, desc=True, joinedCountries=True, joinedCreator=True, hasTag=True, tag=str(tag["id"]))
    return render_template("browse.html", name=name, countries=shared.countries.countries, defaultcountry=form["default_country"], date=form["date"], events=events)

    # Query for events that 