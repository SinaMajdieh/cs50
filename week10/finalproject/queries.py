# Query for selecting last auto increment id from a table
LAST_ID = """SELECT seq FROM sqlite_sequence WHERE name=?;"""


# Query on users table
# -------------------------------------------------------------------
# Query for selecting a all users by username
SELECT_ALL_USERS_INFO_BY_USERNAME = "SELECT * FROM users WHERE username = ?;"

# Query for inserting a new row into users
INSERT_NEW_USER = "INSERT INTO users (username, hash) VALUES (?, ?);"


# Query on events table
# -------------------------------------------------------------------
# Declaring all valid colums of event table to make sure refrences are valid
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

# Query for selecting all event from the events table where id is given
SELECT_ALL_EVENTS_BY_ID = """SELECT * FROM events WHERE id = ? AND state = ?;"""

# Query for selecting all events from the events table by id joining the country name on it
SELECT_ALL_EVENTS_BY_ID_JOIND_COUNTRIES = """
SELECT events.*, countries.name AS country_name FROM events 
JOIN countries ON events.country_id=countries.id
WHERE events.id = ? AND events.state = ?;
"""

# Query for all selecting all events from the events table where id is given joining the username from the users table on it
SELECT_ALL_EVENTS_BY_ID_JOINED_USERS = """
SELECT events.*, users.username FROM events
JOIN users ON events.creator_id=users.id
WHERE events.id = ? AND state = ?;
"""

# Query for selecting all events from the events table where user id is given
SELECT_ALL_EVENTS_BY_USER_ID = """SELECT * FROM events WHERE creator_id = ? AND state = ? ORDER BY timestamp DESC;"""

# Query for inserting a row into the events table
INSERT_EVENT = """
INSERT INTO events 
(title, country_id, creator_id , details, date, cap, enroled, state, timestamp, tags) 
VALUES
(?, ?, ?, ?, ?, ?, ? ,?, ?, ?);
"""

# Query for selecting all events from the events table where id and creator id is given
SELECT_BY_EVENT_ID_USER_ID = """SELECT * FROM events WHERE id = ? AND creator_id = ? AND state = ?;"""

# Will not remove any rows just update the state
DELETE_EVENT = """UPDATE events SET state = ? WHERE id = ?;"""
SELECT_EVENTS_USER_ENROLED = """
SELECT events.* FROM events JOIN
entry ON events.id=entry.event_id WHERE entry.user_id = ?;
"""


# Querry on entry table
# -------------------------------------------------------------------
# Declaring all entry table columns to ensure all refrences are valid
entry_columns = [
    "id",
    "user_id",
    "event_id",
    "timestamp",
]

# Query to insert a new row into the entry table
INSERT_ENTRY = """
INSERT INTO entry 
(user_id, event_id, timestamp)
VALUES
(?, ?, ?);
""" 

# Query for selecting all events joining username from users id and displaying events according to user's state regarding event
# Ordering them by timestamp
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

# Query for selecting all events user has enrolled in
SELECT_EVENTS_USER_ENROLED = """
SELECT events.* FROM events
JOIN entry ON events.id = entry.event_id
WHERE entry.user_id = ? AND events.state = ?;
"""

# Query for selecting all events user has enrolled in joining the country name
SELECT_EVENTS_USER_ENROLED_JOINED_COUNTRIES = """
SELECT events.*, countries.name AS country_name FROM events
JOIN entry ON events.id = entry.event_id
JOIN description ON entry.user_id = description.user_id
JOIN countries ON description.country_id=countries.id
WHERE entry.user_id = ? AND events.state = ?;
"""

# Query for deleting from entry by user id and event id
DELETE_ENTRY_BY_USER_BY_EVENT = """DELETE FROM entry WHERE user_id = ? AND event_id = ?;"""

# Query for deleting from entry by user id and event id
DELETE_EVENT_ENTRY = """DELETE FROM entry WHERE event_id = ?;"""


# Query on description table
# -------------------------------------------------------------------
# Query to insert a new row into description table
INSERT_DESCRIPTION = "INSERT INTO description (name, lastname, email, age, user_id, country_id) VALUES (?, ?, ?, ?, ?, ?);"

# Query for selecting all descriptions where email is given
SELECT_ALL_DESCRIPTION_BY_EMAIL = """SELECT * FROM description WHERE email = ?;"""


# Query on countries table
# -------------------------------------------------------------------
# Query for selecting all countries from the country table 
SELECT_ALL_COUNTRIES = "SELECT * FROM countries;"

# Query for selecting country information of a user
USER_ID_USER_COUNTRY = "SELECT countries.* FROM countries JOIN description ON countries.id=description.country_id WHERE description.user_id = ?;"


# Query on tags tabl
# -------------------------------------------------------------------
# Query for selecting all tags from the tags table
SELECT_ALL_TAGS = """SELECT * FROM tags;"""


# Query on stats table
# -------------------------------------------------------------------
# Query for selecting all stats from the stats table
SELECT_ALL_STATS = """SELECT * FROM stats;"""