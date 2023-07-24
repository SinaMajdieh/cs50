LAST_ID = """SELECT seq FROM sqlite_sequence WHERE name=?;"""
# Query on users table
GET_ALL_USERS_INFO_BY_USERNAME = "SELECT * FROM users WHERE username = ?;"
INSERT_NEW_USER = "INSERT INTO users (username, hash) VALUES (?, ?);"

# Query on events table
event_columns = [
    "id",
    "title",
    "country_id",
    "creator_id",
    "details",
    "date",
    "cap",
    "enroled",
    "state",
    "timestamp",
    "tags"
    ]
SELECT_ALL_EVENTS_BY_ID = """SELECT * FROM events WHERE id = ? AND state = ?;"""
SELECT_ALL_EVENTS_BY_ID_JOIND_COUNTRIES = """
SELECT events.*, countries.name AS country_name FROM events 
JOIN countries ON events.country_id=countries.id
WHERE events.id = ? AND events.state = ?;
"""
SELECT_ALL_EVENTS_BY_ID_JOINED_USERS = """
SELECT events.*, users.username FROM events
JOIN users ON events.creator_id=users.id
WHERE events.id = ? AND state = ?;
"""
SELECT_ALL_EVENTS_BY_USER_ID = """SELECT * FROM events WHERE creator_id = ? AND state = ? ORDER BY timestamp DESC;"""
INSERT_EVENT = """
INSERT INTO events 
(title, country_id, creator_id , details, date, cap, enroled, state, timestamp, tags) 
VALUES
(?, ?, ?, ?, ?, ?, ? ,?, ?, ?);
"""
SELECT_BY_EVENT_ID_USER_ID = """SELECT * FROM events WHERE id = ? AND creator_id = ? AND state = ?;"""
# Will not remove any rows just update the state
DELETE_EVENT = """UPDATE events SET state = ? WHERE id = ?;"""
SELECT_EVENTS_USER_ENROLED = """
SELECT events.* FROM events JOIN
entry ON events.id=entry.event_id WHERE entry.user_id = ?;
"""

# Querry on entry table
entry_columns = [
    "id",
    "user_id",
    "event_id",
    "timestamp",
]
INSERT_ENTRY = """
INSERT INTO entry 
(user_id, event_id, timestamp)
VALUES
(?, ?, ?);
""" 
SELECT_ALL_ENTRIES_BY_EVENT_ID_JOINED_USERS = """
SELECT entry.*, users.username,
    IIF(entry.user_id = ?, 
            1,
            2 
        ) display
FROM entry
JOIN users ON entry.user_id=users.id
JOIN events ON entry.event_id=events.id
WHERE entry.event_id = ? AND events.state = ? ORDER BY timestamp DESC;
"""
SELECT_EVENTS_USER_ENROLED = """
SELECT events.* FROM events
JOIN entry ON events.id = entry.event_id
WHERE entry.user_id = ? AND events.state = ?;
"""


# Query on description table
INSERT_DESCRIPTION = "INSERT INTO description (name, lastname, email, age, user_id, country_id) VALUES (?, ?, ?, ?, ?, ?);"
SELECT_ALL_DESCRIPTION_BY_EMAIL = """SELECT * FROM description WHERE email = ?;"""

# Query on countries table
SELECT_ALL_COUNTRIES = "SELECT * FROM countries;"
USER_ID_USER_COUNTRY = "SELECT countries.* FROM countries JOIN description ON countries.id=description.country_id WHERE description.user_id = ?;"

# Query on tags table
SELECT_ALL_TAGS = """SELECT * FROM tags;"""

# QUery on stats table
SELECT_ALL_STATS = """SELECT * FROM stats;"""