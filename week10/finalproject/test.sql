SELECT events.* ,
IIF(entry.user_id = ?, 
    1,
    IIF(events.date = ? AND events.country_id = ?,
        2,
        0
    )  
) display
FROM events JOIN
entry ON events.id=entry.event_id WHERE display != 0 ORDER BY display ASC;


SELECT events.* ,
IIF(entry.user_id = 8, 
    1,
    IIF(events.date = "2023-07-24" AND events.country_id = 82,
        2,
        0
    )  
) display
FROM events JOIN
entry ON events.id=entry.event_id WHERE display != 0 ORDER BY display ASC;


SELECT events.* ,
            IIF(entry.user_id = 8, 
                1,
                IIF( events.country_id = 82 AND events.date = "2023-07-24" AND events.state = 1,
                    2,
                    0
                )  
            ) display
            FROM events JOIN
            entry ON events.id=entry.event_id WHERE display != 0 ORDER BY display ASC, date 
        DESC;


        SELECT events.* , countries.name AS country_name , users.username AS username,
            IIF(entry.user_id = 12, 
                1,
                IIF(events.country_id = 184 AND events.date = '2023-07-26' AND events.state = 1,
                    2,
                    0
                )  
            ) display
            FROM events 
            JOIN entry ON events.id=entry.event_id
            JOIN countries ON events.country_id=countries.id  
            JOIN users ON events.creator_id=users.id 
            WHERE display != 0 GROUP BY events.id ORDER BY display ASC, date 
        DESC;