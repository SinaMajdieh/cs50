import sys
from cs50 import SQL
from queries import *

class Sqlitedb:
    def __init__(self, path):
        """initate sqlite3 database"""
        self.db = open_sqlite_database(path)
      
    # Query sqlite_sequence for the last AUTOINCREMENT field where table equals to the table
    def lastId(self, table):
        return self.db.execute(LAST_ID, table)
      

    # Functions on users table
    
    # Querry users table for all the columns where username is equal to the username
    def getUserByUsername(self, username):
        return self.db.execute(GET_ALL_USERS_INFO_BY_USERNAME, username)


    # Query users table, inserting anew row
    def insertUser(self, username, password_hash):
        return self.db.execute(INSERT_NEW_USER, username, password_hash)


    # Functions on events table
    
    
    def getEventsUserEnroledAndAvailable(self, user_id, form, desc=True, joinedCountries=False, joinedCreator=False):
        
        order = "DESC"
        if not desc:
            order = "ASC"
        joinedCountryQuery = ""
        joinedCountryColumn = ""
        if joinedCountries:
            joinedCountryQuery = "JOIN countries ON events.country_id=countries.id "
            joinedCountryColumn = ", countries.name AS country_name"
        joinedCreatorQuery = ""
        joinedCreatorColumn = ""    
        if joinedCreator:
            joinedCreatorQuery = "JOIN users ON events.creator_id=users.id "
            joinedCreatorColumn = ", users.username AS username"  
        clauses = []
        values = [user_id]
        for key in form:
            if key in event_columns:
                clauses.append("events." + key + " = ?")
                values.append(form[key])
        clause = " AND ".join(clauses)
        query = f"""
        SELECT events.* {joinedCountryColumn} {joinedCreatorColumn},
            IIF(entry.user_id = ?, 
                1,
                IIF({clause},
                    2,
                    0
                )  
            ) display
            FROM events 
            JOIN entry ON events.id=entry.event_id
            {joinedCountryQuery} 
            {joinedCreatorQuery}
            WHERE display != 0 GROUP BY events.id ORDER BY display ASC, date 
        """ + order + ", events.timestamp DESC;"
        return self.db.execute(query, *values)
    
    

    # Querry events table for all the columns where event id equals the id
    def getEventById(self, id, state, joinedCountries=False):
        query = SELECT_ALL_EVENTS_BY_ID
        if joinedCountries:
            query = SELECT_ALL_EVENTS_BY_ID_JOIND_COUNTRIES
        return self.db.execute(query, id, state)
    
    def getEventByIdJoinedUsers(self, id, state):
        return self.db.execute(SELECT_ALL_EVENTS_BY_ID_JOINED_USERS, id, state)
    
    
    # Query events table for all the columns where creator id equals the id
    def getEventByUserId(self, id, state):
        return self.db.execute(SELECT_ALL_EVENTS_BY_USER_ID, id, state)

    
    # Query events table to insert a new row of data in format of a dict    
    def insertEvent(self, form):
        return self.db.execute(INSERT_EVENT, 
                               form["title"],
                               form["country_id"],
                               form["creator_id"],
                               form["details"],
                               form["date"],
                               form["cap"],
                               form["enroled"],        
                               form["state"],
                               form["timestamp"],
                               form["tags"],
                               )
    
    
    # Query events table for all columns where id and creator id are given
    def eventByIdUserId(self, id, creator_id, state):
        return self.db.execute(SELECT_BY_EVENT_ID_USER_ID, id, creator_id, state)
    
    
    # Query events table for all the columns where country id is given
    def getEventsCustom(self, form, desc=True, joinedCountries = False, joinedCreator = False):
        order = "DESC"
        if not desc:
            order = "ASC"
        joinedCountriesQuery = ""
        joinedCountryColumn = ""
        if joinedCountries:
            joinedCountriesQuery = " JOIN countries ON events.country_id=countries.id "
            joinedCountryColumn = " , countries.name AS country_name "
        joinedCreatorQuery = ""
        joinedCreatorColumn = ""    
        if joinedCreator:
            joinedCreatorQuery = " JOIN users ON events.creator_id=users.id "
            joinedCreatorColumn = " , users.username AS username "  
        query = "SELECT events.*" + joinedCountryColumn + joinedCreatorColumn + "FROM events" + joinedCountriesQuery + joinedCreatorQuery
        clauses = []
        values = []
        for key in form:
            if key in event_columns:
                clauses.append(key + " = ?")
                values.append(form[key])
        query = query + " WHERE " + " AND ".join(clauses) + " ORDER BY date " + order + ", events.timestamp DESC;"
        return self.db.execute(query, *values)
    
    
    # Update certain attributes of a row
    def updateEventCustomById(self, id, form):
        try:
            # adding columns and attributes only if they are a valid column
            query = "UPDATE events"
            clauses = []
            values = []
            for key in form:
                if key in event_columns:
                    clauses.append(key + " = ?")
                    values.append(form[key])
            query = query + " SET " + ", ".join(clauses) + " WHERE id = ?;"
            values.append(id)
            self.db.execute(query, *values)
            
            return True
        except:
            return False


    def selectEventUserEnroled(self, id):
        return self.db.execute(SELECT_EVENTS_USER_ENROLED, id)


    # Delete an event (actually updating the state to delete) will not remove any rows
    def changeEventState(self, id, state_id):
        return self.db.execute(DELETE_EVENT, state_id, id)
    
    
    # Functions on entry table
    def insertEntry(self, form):
        self.db.execute(INSERT_ENTRY,
                        form["user_id"],
                        form["event_id"],
                        form["timestamp"],
                        )
    
    
    def getEntryCustome(self, form):
        query = "SELECT * FROM entry"
        clauses = []
        values = []
        for key in form:
            if key in entry_columns:
                clauses.append(key + " = ?")
                values.append(form[key])
        query = query + " WHERE " + " AND ".join(clauses) + ";"
        return self.db.execute(query, *values)
        

    def getEntriesByEventIdJoinedUsers(self, user_id, event_id, state):
        return self.db.execute(SELECT_ALL_ENTRIES_BY_EVENT_ID_JOINED_USERS, user_id, event_id, state)


    def getEventsUserEnroled(self, user_id, state):
        return self.db.execute(SELECT_EVENTS_USER_ENROLED, user_id, state)

    # Functions on description table
    
    # Query description table for all the columns where the email equlas email
    def getDescriptionByEmail(self, email):
        return self.db.execute(SELECT_ALL_DESCRIPTION_BY_EMAIL, email)
    
    
    # Query description table to insert a new row of data in format of a dict 
    def insertDescription(self, form):
        return self.db.execute(INSERT_DESCRIPTION,
                               form["name"],
                               form["lastname"],
                               form["email"],
                               form["age"] ,
                               form["user_id"],
                               form["country"])
    

    # Functions on countries table   
    
    # Query countries table for all the columns of all rows
    def load_countries(self):
        """Load all country lists from sqlte3 into memory"""
        return self.db.execute(SELECT_ALL_COUNTRIES)


    # Query database for the users country
    def getCountryByUserId(self, id):
        return self.db.execute(USER_ID_USER_COUNTRY, id)
    
    
    # Functions on tags table
    
    # Query tags table for all the colums of all rows
    def load_tags(self):
        return self.db.execute(SELECT_ALL_TAGS)
    
    # Functions on stats table
    
    # Query stats table for all the columns of all rows
    def load_stats(self):
        return self.db.execute(SELECT_ALL_STATS)
    

def open_sqlite_database(path):
    """Opening the sqlite3 database"""
    return SQL("sqlite:///"+path)


