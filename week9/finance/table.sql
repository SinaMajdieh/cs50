/*CREATE TABLE transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    time_stamp TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    type TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE holdings(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);*/
INSERT INTO users username,hash, cash,
    case when COUNT((SELECT )) != 0
    then cash
    ELSE 'found'
    End as result
FROM users;
