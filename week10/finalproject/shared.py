from database import Sqlitedb

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
        
        
    def lookup_title(self, title):
        """
        Looks up a tag by its name
        returning the tag if it was found
        return None if it wasnt
        """

        for tag in self.tags:
            if tag["title"] == title:
                return tag
            
        return None

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