import os
import sys
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# sql querry creating transaction table if it does not exist
TRANSACTION_TABLE = """
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    time_stamp TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER,
    type TEXT NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""
# sql querry creating transaction table if it does not exist
HOLDINGS_TABLE = """
CREATE TABLE IF NOT EXISTS holdings(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""


def create_tables():
    """running transaction and holdings table creation"""
    db.execute(TRANSACTION_TABLE)
    db.execute(HOLDINGS_TABLE)
    

def rn():
    """returns current time in the DD/MM/YYYY HH:MM:SS format"""
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    return current_time


# sqlite querries
TABLES_EXIST = False
USER_HASH_PASS = "SELECT hash FROM users WHERE id = ?;"
UPDATE_USER_PASS = "UPDATE users SET hash = ? WHERE id = ?;"
ALL_USER_HOLDINGS = "SELECT symbol, shares FROM holdings WHERE user_id = ? ORDER BY shares DESC;"
USER_CASH = "SELECT cash FROM users WHERE id = ?;"
UPDATE_USER_CASH = "UPDATE users SET cash = ? WHERE id = ?;"
INSERT_TRANSACTION = "INSERT INTO transactions (time_stamp, user_id, symbol, shares, type, price) VALUES (?, ?, ?, ?, ?, ?);"
CHECK_HOLDING_SHARES = "SELECT shares from holdings WHERE user_id = ? AND symbol = ?;"
ADD_HOLDING = "INSERT INTO holdings (user_id, symbol, shares) VALUES (?, ?, ?);"
UPDATE_HOLDING = "UPDATE holdings SET shares = ? WHERE user_id = ? AND symbol = ?;"
DELET_HOLDING = "DELETE FROM holdings WHERE shares = ?;"
USER_TRANSACTIONS = "SELECT time_stamp, symbol, shares, type, price FROM transactions WHERE user_id = ? ORDER BY time_stamp;"
USERNAME_EQUALS = "SELECT username FROM users WHERE username = ?;"
INSERT_NEW_USER = "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?);"
STOCK_IN_USER_HOLDINGS = "SELECT symbol, shares FROM holdings WHERE user_id = ? AND symbol = ?;"


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    
    holdings = db.execute(ALL_USER_HOLDINGS, session["user_id"])
    cash = db.execute(USER_CASH, session["user_id"])[0]["cash"]
    
    holdings_form = []
    holdings_value = 0
    for holding in holdings:
        price = lookup(holding["symbol"])["price"]
        total_price = price * holding["shares"]
        entry = {
            "symbol": holding["symbol"],
            "shares": holding["shares"],
            "price": usd(price),
            "total": usd(total_price),   
        }
        holdings_form.append(entry)
        holdings_value += total_price
        
    return render_template("index.html", exists=bool(holdings), holdings=holdings_form, cash=usd(cash), total=usd(holdings_value+cash))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # clear the last session
    session.clear()
    
    # if the method is GET then go to the registration page
    if request.method == "GET":
        return render_template("register.html")
    else:
        
        # extrating the values submited via form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # if the user didn't fill out all the fields
        if not username or not password or not confirmation:
            return apology("Make sure to fill out all the fields")
        
        # if the username was taken
        if len(db.execute(USERNAME_EQUALS, username)) != 0:
            return apology("username already exists")
        
        # if the confirmation does not match the original password 
        if confirmation != password:
            return apology("confirmation does not match the password")
        
        # hash the users password
        password_hash = generate_password_hash(password)
        
        # insert the new user
        db.execute(INSERT_NEW_USER, username, password_hash, 10000)
        
        return redirect("/login")               
    

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepass():
    """Change users passsword"""
    # GET method renders a form for changing the password
    if request.method == "GET":
        return render_template("changepasswordform.html")
    else:
        # getting old password and the new password and the confirmation from the parsed from
        oldpass = request.form.get("oldpass")
        newpass = request.form.get("newpass")
        confirm = request.form.get("confirmation")
        
        # None values return an apology
        if not oldpass or not newpass or not confirm:
            return apology("Make sure to fill out all the fields")
        
        # password hash retrieved from the sqlite database
        passhash = db.execute(USER_HASH_PASS, session["user_id"])
        passhash = passhash[0]["hash"]
        
        # password does not match the hash -> wrong password
        if not check_password_hash(passhash, oldpass):
            return apology("Wrong password")
        # new password matchs the hash -> new password is the old password
        if check_password_hash(passhash, newpass):
            return apology("your new password is your old password")
        # confirmation does not match the new password
        if confirm != newpass:
            return apology("your new password does not match the confirmation")
        # updating the new password hash in the sqlite database
        db.execute(UPDATE_USER_PASS, generate_password_hash(newpass), session["user_id"])
        # prompting the user -> password changed successfuly
        flash("Password Changed")
        # redireting to the homepage
        return redirect("/")

 
@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """add more cash"""
    # GET method renders a form to add more cash
    if request.method == "GET":
        return render_template("depositform.html")
    else:
        # create tables (transactions and holdings) if they dont exist
        global TABLES_EXIST
        if not TABLES_EXIST:
            create_tables()
            TABLES_EXIST = True
            
        # getting cash password and the confirmation from the parsed form
        cash = request.form.get("cash")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        
        # None values return an apology
        if not cash or not password or not confirm:
            return apology("Make sure to fill out all the fields")
        
        # trying to convert the cash from parsed form to an integer
        try:
            cash = int(cash)
            # cash should be greater than 0
            if cash <= 0:
                return apology("The deposit amount shoul be a positive integer")
        except ValueError:
            # cash could not be converted to an integer returning an apology
            return apology("The deposit amount shoul be a positive integer")
        
        # retreiving the password hash from the sqlite database
        passhash = db.execute(USER_HASH_PASS, session["user_id"])
        passhash = passhash[0]["hash"]
        
        # password and hash do not match -> wrong password
        if not check_password_hash(passhash, password):
            return apology("Wrong password")
        
        # password and the confirmation does not match
        if confirm != password:
            return apology("confirmation does not match the password")
        
        # retreiving user cash from the sqlite database
        user_cash = db.execute(USER_CASH, session["user_id"])[0]["cash"]
        
        # updating the user cash in the users table in the sqlite database
        # inserting the new transaction into the transactions table in the sqlite database
        db.execute(UPDATE_USER_CASH, user_cash+cash, session["user_id"])
        db.execute(INSERT_TRANSACTION, rn(), session["user_id"], "", None, "deposit", cash)
        
        # prompting the user process was successful and how much they've deposited
        flash("You deposited " + usd(cash))
        
        # redirectung to the homepage
        return redirect("/")
        

@app.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    "withdraw cash"
    # GET method renders a form to withdraw cash
    if request.method == "GET":
        return render_template("withdrawform.html")
    else:
        # create tables (transactions and holdings) if they dont exist
        global TABLES_EXIST
        if not TABLES_EXIST:
            create_tables()
            TABLES_EXIST = True
            
        # getting cash, password, confirmation from the parsed form
        cash = request.form.get("cash")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        
        # None values return an apology
        if not cash or not password or not confirm:
            return apology("Make sure to fill out all the fields")
        
        # trying to convert the cash from parsed form to an integer
        try:
            cash = int(cash)
            # cash should be greater than 0
            if cash <= 0:
                return apology("The withdraw amount shoul be a positive integer")
        except ValueError:
            # cash could not be converted to an integer returning an apology
            return apology("The withdraw amount shoul be a positive integer")
        
        # retreiving the password hash from the sqlite database
        passhash = db.execute(USER_HASH_PASS, session["user_id"])
        passhash = passhash[0]["hash"]
        
        # password and hash do not match -> wrong password
        if not check_password_hash(passhash, password):
            return apology("Wrong password")
        
        # password and the confirmation does not match
        if confirm != password:
            return apology("confirmation does not match the password")
        
        # retreiving user cash from the sqlite database
        user_cash = db.execute(USER_CASH, session["user_id"])[0]["cash"]
        
        # user's cash sould be greater or eaqual than the cash they want to withdraw
        if user_cash < cash:
            return apology("You dont have enogh cash in your balance")
        
        # updating the user cash in the users table in the sqlite database
        # inserting the new transaction into the transactions table in the sqlite database
        db.execute(UPDATE_USER_CASH, user_cash-cash, session["user_id"])
        db.execute(INSERT_TRANSACTION, rn(), session["user_id"], "", None, "withdraw", cash)
        
        # prompting the user process was successful and how much they've withdrawed
        flash("You withdrawed " + usd(cash))
        
        # redircting to the homepage
        return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # GET method renders a form to get a stocks information
    if request.method == "GET":
        return render_template("quote.html")
    else:
        # getting stock symbol from the parsed form
        stocksym = request.form.get("symbol")
        
        # None values return an apology
        if not stocksym:
            return apology("Make sure to fill out all the fields") 
        
        # look up the stock
        stockres = lookup(stocksym)
        
        # stock does not exist or was not found -> reaturn an apology prompting the user  
        if not stockres:
            return apology("Couldn't Find stock")
        
        # stock was found render the stocks infromation
        return render_template("quoted.html", symbol=stocksym, found=bool(stockres), stock=stockres)
    

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # GET method renders a form to withdraw cash
    if request.method == "GET":
        return render_template("buyform.html")
    else:
        # create tables (transactions and holdings) if they dont exist
        global TABLES_EXIST
        if not TABLES_EXIST:
            create_tables()
            TABLES_EXIST = True
            
        # getting cash, password, confirmation from the parsed form
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        
        # None values return an apology
        if not symbol or not shares:
            return apology("Make sure to fill out all the fields")
        
        # trying to convert the shares from parsed form to an integer
        try:
            shares = int(shares)
            # shares should be greater than 0
            if shares <= 0:
                return apology("shares should be positive integers")
        except ValueError:
            # shares could not be converted to an integer returning an apology
            return apology("shares should be positive integers")
        
        # look up the stocks information
        stock = lookup(symbol)
        
        # stocks does not exist or was not found -> return an apology prompting the user
        if not stock:
            return apology("stock does not exist")
        
        # retreiving the symbol of the stock
        symbol = stock["symbol"]
        
        # calculating how much the price is for the total shares
        charge = shares * stock["price"]
        
        # retreiving the user cash from the users in the sqite database
        user_cash = db.execute(USER_CASH, session["user_id"])
        user_cash = user_cash[0]["cash"]
        
        # user shoul have enough money to purchase the shares
        if charge > user_cash:
            return apology("Not enough cash")
        
        # insering the new transaction to the transactions table in the sqlite database
        db.execute(INSERT_TRANSACTION, rn(), session["user_id"], symbol, shares, "buy", charge)
        db.execute(UPDATE_USER_CASH, user_cash-charge, session["user_id"])
        
        # retreiving how many shares of the stock user already owns
        owened_shares = db.execute(CHECK_HOLDING_SHARES, session["user_id"], symbol)
        
        # user dont own any -> add it to their holdings
        if not owened_shares:
            db.execute(ADD_HOLDING, session["user_id"], symbol, shares)
        else:
            # adding to the existing shares
            pre_shares = owened_shares[0]["shares"]
            db.execute(UPDATE_HOLDING, pre_shares+shares, session["user_id"], symbol)
        
        # prompting the user the purchase was successful
        flash("Bought!")
        
        # redirecting the user to the homepage
        return redirect("/")       


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # GET method renders a form to withdraw cash
    if request.method == "GET":
        holdings = db.execute(ALL_USER_HOLDINGS, session["user_id"])
        return render_template("sellform.html", exists=bool(holdings), stocks=holdings)
    else:
        # create tables (transactions and holdings) if they dont exist
        global TABLES_EXIST
        if not TABLES_EXIST:
            create_tables()
            TABLES_EXIST = True
            
        # getting cash, password, confirmation from the parsed form
        symbol = request.form.get("symbol")
        shares = request.form.get("shares") 
        
        # None values return an apology
        if not symbol or not shares:
            return apology("Make sure to fill out all fields")
        
        # trying to convert the shares from parsed form to an integer
        try:
            shares = int(shares)
            # shares should be greater than 0
            if shares <= 0:
                return apology("shares should be positive integers")
        except ValueError:
            return apology("shares should be positive integers")
            # shares could not be converted to an integer returning an apology
        
        # look up the stock the user wants to sell
        stock = lookup(symbol)
        
        # retreive the stock user claims they own from the holdings table in the sqlite database
        holding = db.execute(STOCK_IN_USER_HOLDINGS, session["user_id"], symbol) 
        
        # the stock does not exist or was foun or the user do not own any shares of the stock they want to sell -> return an apology
        if not holding or not stock:
            return apology("you dont own any shares of "+symbol+" or it does not exist")
        holding = holding[0]
        
        # user should have enough shares
        if shares > holding["shares"]:
            return apology(f"""You dont own {shares} shares""")
        
        # calculating how much the price is for the total shares
        price = shares * stock["price"]
        
        # insering the new transaction to the transactions table in the sqlite database    
        db.execute(INSERT_TRANSACTION, rn(), session["user_id"], symbol, shares, "sell", price)
        # update the user holding in the holdings table in the sqlite3 database
        db.execute(UPDATE_HOLDING, holding["shares"]-shares, session["user_id"], symbol)
        # delete the stock where the user owns 0 of
        db.execute(DELET_HOLDING, 0)
        
        # retreive the user's cash from the users table in the sqlite3 database
        cash = db.execute(USER_CASH, session["user_id"])
        cash = cash[0]["cash"]
        
        # update the user's cash in the users table in the sqlite3 database                  
        db.execute(UPDATE_USER_CASH, cash + price, session["user_id"])
        
        # prompting the user the sale was successful
        flash("Sold")
        
        # redirecting to the homepage
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # retreive the user's transactions from the transactions table in the sqlite3 database
    transactions = db.execute(USER_TRANSACTIONS, session["user_id"])
    
    # a list of the formatted transactions
    transactions_formatted = []
    
    # format every transaction and add it to the list
    for transaction in transactions:
        # formatting the transactions
        entry = {
            "date": transaction["time_stamp"],
            "name": transaction["symbol"],
            "shares": transaction["shares"],
            "price": transaction["price"],
            "transaction": transaction["type"]
        }
        # inserting them into the begenning of the list
        transactions_formatted.insert(0, entry)
    
    # rendering the results to the client
    return render_template("history.html", exists=bool(transactions_formatted), transactions=transactions_formatted)

