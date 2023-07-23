from cs50 import SQL
from queries import *

class Sqlitedb:
    def __init__(self, path):
        """initate sqlite3 database"""
        self.db = open_sqlite_database(path)
      
      
    def lastId(self, table):
        return self.db.execute(LAST_ID, table)
      

    # Functions on users table
    def getUserByUsername(self, username):
        return self.db.execute(GET_ALL_USERS_INFO_BY_USERNAME, username)


    def insertUser(self, username, password_hash):
        return self.db.execute(INSERT_NEW_USER, username, password_hash)


    # Functions on events table
    def getEventById(self, id):
        return self.db.execute(SELECT_ALL_EVENTS_BY_ID, id)
    
    
    def getEventByUserId(self, id):
        return self.db.execute(SELECT_ALL_EVENTS_BY_USER_ID, id)
    
    
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
        
    


    # Functions on entry table
    def insertEntry(self, form):
        self.db.execute(INSERT_ENTRY,
                        form["user_id"],
                        form["event_id"],
                        form["timestamp"],
                        )

    # Functions on description table
    def getDescriptionByEmail(self, email):
        return self.db.execute(SELECT_ALL_DESCRIPTION_BY_EMAIL, email)
    
    
    def insertDescription(self, form):
        return self.db.execute(INSERT_DESCRIPTION, form["name"], form["lastname"], form["email"], form["age"] , form["user_id"], form["country"])
    

    # Functions on countries table   
    def load_countries(self):
        """Load all country lists from sqlte3 into memory"""
        return self.db.execute(SELECT_ALL_COUNTRIES)


    def getCountryByUserId(self, id):
        return self.db.execute(USER_ID_USER_COUNTRY, id)
    
    
    # Functions on tags table
    def load_tags(self):
        return self.db.execute(SELECT_ALL_TAGS)
    

def open_sqlite_database(path):
    """Opening the sqlite3 database"""
    return SQL("sqlite:///"+path)


