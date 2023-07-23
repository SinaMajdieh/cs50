-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Finding the crime description
SELECT description FROM crime_scene_reports
WHERE day = 28 AND month = 7 AND year = 2021
AND street = 'Humphrey Street';

-- Finding out about the transcripts of witnesses
SELECT name, transcript FROM interviews
WHERE day = 28 AND month = 7 AND year = 2021;

-- Finding the parking lot logs of bakery within 10 minutes of the crime
SELECT license_plate, activity FROM bakery_security_logs
WHERE day = 28 AND month = 7 AND year = 2021
AND hour = 10 AND minute >= 5 AND minute <= 25
ORDER BY hour, minute;

-- Finding the atm logs from Leggett street according to witnesses interviews transcript
SELECT account_number, transaction_type FROM atm_transactions
WHERE day = 28 AND month = 7 AND year = 2021
AND atm_location LIKE '%Leggett%'
AND transaction_type = 'withdraw';

-- Finding out about the call that was mentioned in the interviews
SELECT caller, receiver FROM phone_calls
WHERE day = 28 AND month = 7 AND year = 2021
AND duration <= 60;

-- Matching the account numbers with bank account numbers
-- and finding their names and phone numbers 
-- and limiting the output to the ones who left the crime scene within 10 minutes of the crime.
-- and matching those with ones who made a phone call at that time 
SELECT 
atm_transactions.account_number AS Caller_Account,
people.name AS Caller_Name, 
people.passport_number AS Caller_Passport,
people.phone_number AS Caller_Number, 
people.license_plate AS Caller_License,
Receiver_Account,
Receiver_Name,
Receiver_Phone
FROM atm_transactions
JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number
JOIN people ON bank_accounts.person_id = people.id
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
JOIN phone_calls ON people.phone_number = phone_calls.caller
JOIN (
    SELECT 
    people.name AS Receiver_Name,
    bank_accounts.account_number AS Receiver_Account,
    people.phone_number AS Receiver_Phone
    FROM people
    JOIN bank_accounts ON people.id = bank_accounts.person_id  
) ON phone_calls.receiver = Receiver_Phone
WHERE atm_transactions.day = 28 
AND atm_transactions.month = 7 
AND atm_transactions.year = 2021
AND atm_transactions.transaction_type = 'withdraw'
AND atm_location LIKE '%Leggett%'
AND bakery_security_logs.day = 28 
AND bakery_security_logs.month = 7 
AND bakery_security_logs.year = 2021
AND bakery_security_logs.hour = 10 
AND bakery_security_logs.minute >= 5 
AND bakery_security_logs.minute <= 25
AND bakery_security_logs.activity = 'exit'
AND phone_calls.day = 28 
AND phone_calls.month = 7 
AND phone_calls.year = 2021
AND phone_calls.duration <= 60;

-- Finding earliest flights on 29th of July which either 'Philip' or 'Robin' booked
SELECT
flights.id AS flight_id,
from_city,
to_city,
passengers.passport_number,
flights.hour,
flights.minute
FROM flights
JOIN (
    SELECT 
    airports.id AS from_id,
    airports.city AS from_city
    FROM airports
) ON flights.origin_airport_id = from_id
JOIN (
    SELECT 
    airports.id AS to_id,
    airports.city AS to_city
    FROM airports
) ON flights.destination_airport_id = to_id
JOIN passengers ON flights.id = passengers.flight_id
WHERE flights.day = 29 AND flights.month = 7 AND flights.year = 2021
AND from_city = 'Fiftyville'
AND (passengers.passport_number = 3592750733 OR passengers.passport_number = 5773159633)
ORDER BY hour, minute;


