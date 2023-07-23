from datetime import datetime
from flask import render_template
import re

def apology(message, code=400):
    """Render message as an apology to user."""       
    return render_template("apology.html", message=message), code


def right_now():
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    return current_time


def is_country_valid(id, countries):
    """Ensure country name exsist based on the list of dicts containing country id and name"""
    # Ensure country id is not 0
    if id == 0:
        return False
    # Ensure country id is an int
    try:
        id = int(id)
    except ValueError:
        return False
    for country in countries:
        if id == country["id"]:
            return True
    return False
    
def is_email_valid(email):
    """Ensure email is valid"""
    # Ensure email is str
    try:
        email = str(email)
    except ValueError:
        return False
    
    # Ensure email patter is correct
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False
  
def is_age_valid(age):
    """Ensure age input is valid"""
    
    # Ensure age is int
    try:
        age = int(age)
    except ValueError:
        return False
    # Ensure age is above 18
    if age >= 18:
        return True
    else:
        return False
    

def are_tags_valid(ids, tags):
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
        for tag in tags:
            if id == tag["id"]:
                found += 1
    
    
    # Ensure all ids were found in tags
    if found == len(ids):
        return True
    else:
        return False
    
    

def is_cap_valid(cap):
    """Ensure cap is valid"""
    # Ensure cap is an integer
    try:
        cap = int(cap)
    except ValueError:
        return False
    if cap <= 20:
        return True
    else:
        return False