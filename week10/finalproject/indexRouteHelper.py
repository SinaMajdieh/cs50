import sys
from flask import flash, redirect, render_template, request, session
from queries import *
from database import *
from datetime import date
from helpers import apology, is_email_valid, is_age_valid, is_cap_valid, right_now
from werkzeug.security import check_password_hash, generate_password_hash
import shared


def index_filter(form):
    """Replace default values if there is a filter"""
    # Extracting values from sent via get
    country = request.args.get("country")
    date = request.args.get("date")
    
    # user provided the filter with a country
    if country:
        # Ensure country is valid by looking for it
        result = shared.countries.lookup(country)
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
            form["default_country"] = shared.countries.lookup(0)
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
            "state": shared.stats.lookup_key("open"),
        }
        form = index_filter(form)
        events = shared.db.getEventsUserEnroledAndAvailable(session["user_id"], form, desc=True, joinedCountries=True, joinedCreator=True)
        return render_template("index.html", countries=shared.countries.countries, defaultcountry=form["default_country"], date=form["date"], events=events)
    # User has not logged in
    else:
        # country id 0 belong to global
        # apply filter
        form = {
            "date": date.today(),
            "default_country": shared.countries.lookup(0),
            "state": shared.stats.lookup_key("open"),
        }
        form = index_filter(form)
        events = shared.db.getEventsCustom(form, desc=True, joinedCountries=True, joinedCreator=True)
        return render_template("index.html", countries=shared.countries.countries, defaultcountry=form["default_country"], date=form["date"], events=events)
