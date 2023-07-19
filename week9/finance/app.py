import os
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

ALL_USER_HOLDINGS = "SELECT symbol, shares FROM holdings WHERE user_id = ? ORDER BY shares DESC"
USER_CASH = "SELECT cash FROM users WHERE id = ?"
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
                "symbol" : holding["symbol"],
                "shares" : holding["shares"],
                "price" : usd(price),
                "total" : usd(total_price),   
            }
        holdings_form.append(entry)
        holdings_value += total_price
        
    return render_template("index.html", exists=bool(holdings), holdings=holdings_form, cash=usd(cash), total=usd(holdings_value+cash))
    

def rn():
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    return current_time


UPDATE_USER_CASH = "UPDATE users SET cash = ? WHERE id = ?"
INSERT_TRANSACTION = "INSERT INTO transactions (time_stamp, user_id, symbol, shares, type) VALUES (?, ?, ?, ?, ?)"
CHECK_HOLDING_SHARES = "SELECT shares from holdings WHERE user_id = ? AND symbol = ?"
ADD_HOLDING = "INSERT INTO holdings (user_id, symbol, shares) VALUES (?, ?, ?)"
UPDATE_HOLDING = "UPDATE holdings SET shares = ? WHERE user_id = ? AND symbol = ?"
DELET_HOLDING = "DELETE FROM holdings WHERE shares = ?"
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    
    # GET: redirect to the buy form
    # POST: validate anddo the transaction accordingly
    # otherwise wrong method
    if request.method == "GET":
        return render_template("buyform.html")
    elif request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        
        if not symbol or not shares:
            return apology("Make sure to fill out all the fields")
            
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares should be positive integers")
        except ValueError:
            return apology("shares should be positive integers")

        stock = lookup(symbol)
        
        if not bool(stock):
            return apology("stock does not exist")
        
        symbol = stock["name"]
        
        charge = shares * stock["price"]
        
        user_cash = db.execute(USER_CASH, session["user_id"])
        user_cash = user_cash[0]["cash"]
        
        if charge > user_cash:
            return apology("Not enough cash")
        
        db.execute(INSERT_TRANSACTION, rn(), session["user_id"], symbol, shares, "buy")
        db.execute(UPDATE_USER_CASH, user_cash-charge, session["user_id"])
        
        owened_shares = db.execute(CHECK_HOLDING_SHARES, session["user_id"], symbol)
        
        if not owened_shares:
            db.execute(ADD_HOLDING, session["user_id"], symbol, shares)
        else:
            pre_shares = owened_shares[0]["shares"]
            db.execute(UPDATE_HOLDING, pre_shares+shares, session["user_id"], symbol)
            
        
        return redirect("/")
        
        
        
        
    else:
        return apology("Wrong method", 403)
    return apology("TODO")

USER_TRANSACTIONS = "SELECT time_stamp, symbol, shares, type FROM transactions WHERE user_id = ? ORDER BY time_stamp"

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    
    transactions = db.execute(USER_TRANSACTIONS, session["user_id"])
    transactions_formatted = []
    for transaction in transactions:
        entry = {
            "date" : transaction["time_stamp"],
            "name" : transaction["symbol"],
            "shares" : transaction["shares"],
            "price" : lookup(transaction["symbol"])["price"],
            "transaction" : transaction["type"]
        }
        transactions_formatted.insert(0, entry)
    
    return render_template("history.html", exists=bool(transactions_formatted), transactions=transactions_formatted)
    
    


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # GET : redirect user to the search form
    # POST : look up stock and return the result
    # otherwise return wrong method
    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":
        stocksym = request.form.get("symbol")
        
        # check for None value
        if not stocksym:
            return apology("Make sure to fill out all the fields")
        
        #look up the stock
        stockres = lookup(stocksym)
        
        # render the results to the user
        return render_template("quoted.html", symbol=stocksym, found= bool(stockres), stock=stockres)
        
    else:
        return apology("Wrong method", 403)


# querry to check wheter the username already exists
USERNAME_EQUALS = "SELECT username FROM users WHERE username = ?"
INSERT_NEW_USER = "INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)"

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    #clear the last session
    session.clear()
    
    # if the method is GET then go to the registration page
    # otherwise register the new user
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        
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
        
        #insert the new user
        db.execute(INSERT_NEW_USER, username, password_hash, 0)
        
        return redirect("/login")               
    else:
        return apology("Wrong method", 403)
    
    

STOCK_IN_USER_HOLDINGS = "SELECT symbol, shares FROM holdings WHERE user_id = ? AND symbol = ?"


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    
    
    if request.method == "GET":
        holdings = db.execute(ALL_USER_HOLDINGS, session["user_id"])
        return render_template("sellform.html", exists=bool(holdings), stocks=holdings)
    elif request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares") 
       
        if not symbol or not shares:
           return apology("Make sure to fill out all fields")
       
        holding = db.execute(STOCK_IN_USER_HOLDINGS, session["user_id"], symbol)
        
        stock = lookup(symbol)
        
        if not holding or not stock:
            return apology("you dont own any shares of "+symbol+" or it does not exist")
        
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("shares should be positive integers")
        except ValueError:
            return apology("shares should be positive integers")
        
        holding = holding[0]
        
        if shares > holding["shares"]:
            return apology(f"""You dont own {shares} shares""")
        
        price = shares * stock["price"]
        
        db.execute(INSERT_TRANSACTION, rn(), session["user_id"], symbol, shares, "sell")
        db.execute(UPDATE_HOLDING, holding["shares"]-shares, session["user_id"], symbol)
        db.execute(DELET_HOLDING,0)
        
        cash = db.execute(USER_CASH, session["user_id"])
        cash = cash[0]["cash"]
                          
        db.execute(UPDATE_USER_CASH, cash + price, session["user_id"])
        
        return redirect("/")
        
    else:
        return apology("Wrong method", 403)

    
    
