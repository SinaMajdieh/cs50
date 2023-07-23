LAST_ID = """SELECT seq FROM sqlite_sequence WHERE name=?;"""
# Query on users table
GET_ALL_USERS_INFO_BY_USERNAME = "SELECT * FROM users WHERE username = ?;"
INSERT_NEW_USER = "INSERT INTO users (username, hash) VALUES (?, ?);"

# Query on events table
SELECT_ALL_EVENTS_BY_ID = """SELECT * FROM events WHERE id = ?;"""
SELECT_ALL_EVENTS_BY_USER_ID = """SELECT * FROM events WHERE creator_id = ? ORDER BY date ASC;"""
INSERT_EVENT = """
INSERT INTO events 
(title, country_id, creator_id , details, date, cap, enroled, state, timestamp, tags) 
VALUES
(?, ?, ?, ?, ?, ?, ? ,?, ?, ?);
"""

# Querry on entry table
INSERT_ENTRY = """
INSERT INTO entry 
(user_id, event_id, timestamp)
VALUES
(?, ?, ?);
""" 

# Query on description table
INSERT_DESCRIPTION = "INSERT INTO description (name, lastname, email, age, user_id, country_id) VALUES (?, ?, ?, ?, ?, ?);"
SELECT_ALL_DESCRIPTION_BY_EMAIL = """SELECT * FROM description WHERE email = ?;"""

# Query on countries table
SELECT_ALL_COUNTRIES = "SELECT * FROM countries;"
USER_ID_USER_COUNTRY = "SELECT countries.* FROM countries JOIN description ON countries.id=description.country_id WHERE description.user_id = ?;"

# Query on tags table
SELECT_ALL_TAGS = """SELECT * FROM tags;"""