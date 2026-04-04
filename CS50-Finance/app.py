import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
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

timestamp = datetime.datetime.now()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # get user's stocks and balance
    transactions_db = db.execute(
        "SELECT symbol, SUM(shares) as shares, price FROM transactions WHERE user_id = ? GROUP BY symbol",
        user_id,
    )

    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

    # get user's cash's balance
    cash = cash_db[0]["cash"]

    # initialize variables for total values
    total_value = cash
    grand_total = cash

    for stock in transactions_db:
        quote = lookup(stock["symbol"])

        value = stock["shares"] * stock["price"]
        total_value += value
        grand_total += value
        print(f"Updated cash balance: {cash}")

    return render_template(
        "index.html",
        database=transactions_db,
        cash=cash,
        total_value=total_value,
        grand_total=grand_total,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")

        try:
            shares = request.form.get("shares")
            shares = int(shares)

        except:
            return apology("Shares must be a positive integer")

        if not symbol:
            return apology("Must Give Symbol")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Symbol Does Not Exist")

        if shares < 0:
            return apology("Share Not Allowed")

        transaction_value = shares * stock["price"]
        # user must be legit
        user_id = session["user_id"]
        # extract cash info. from that user's database
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        # see if the amount of cash is sufficient
        if user_cash < transaction_value:
            return apology("Not Enough Money")
        # deduct the money amount
        uptd_cash = user_cash - transaction_value
        # update the balance cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)

        date = datetime.datetime.now()

        # now update the data in the transaction table
        # here user_id is not username it got from the session
        # The user_id stored in the session is typically a unique identifier for the user
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
            user_id,
            stock["symbol"],
            shares,
            stock["price"],
            timestamp,
        )

        flash("Bought!")

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions_db = db.execute(
        "SELECT * FROM transactions WHERE user_id = :id", id=user_id
    )
    return render_template("history.html", transactions=transactions_db)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Must Give Symbol")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Symbol Does Not Exist")
        return render_template(
            "quoted.html", price=stock["price"], symbol=stock["symbol"]
        )


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    # ensure the user reaches via post i.e. has submitted form in register.html
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Must Give Username")

        if not password:
            return apology("Must Give Password")
        # ensure password confirmation was submitted
        if not confirmation:
            return apology("Must Give Confirmation")
        # ensure password and confirmation match
        if password != confirmation:
            return apology("Password Do Not Match")

        # create a hashed version of a password
        hash = generate_password_hash(password)

        try:
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash
            )
        except:
            # username already exists,so insertion would fail and will return apology api meme
            return apology("Username already exists")

        # stores the new user's ID in the session.
        session["user_id"] = new_user

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
            user_id,
        )
        return render_template(
            "sell.html", symbols=[row["symbol"] for row in symbols_user]
        )
    else:
        # we get symbol and shares from the form
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("Must Give Symbol")

        stock = lookup(symbol.upper())

        if stock == None:
            return apology("Symbol Does Not Exist")

        if shares < 0:
            return apology("Share Not Allowed")

        transaction_value = shares * stock["price"]

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        user_shares = db.execute(
            "SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",
            user_id,
            symbol,
        )
        user_shares_real = user_shares[0]["shares"]

        if shares > user_shares_real:
            return apology("You Do Not Have This Amount Od Shares")

        uptd_cash = user_cash + transaction_value

        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)

        date = datetime.datetime.now()

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, timestamp) VALUES (?, ?, ?, ?, ?)",
            user_id,
            stock["symbol"],
            (-1) * shares,
            stock["price"],
            date,
        )

        flash("Sold!")

        return redirect("/")


# additonal to add cash


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """User can add cash"""
    if request.method == "GET":
        return render_template("add.html")
    else:
        new_cash = int(request.form.get("new_cash"))

        if not new_cash:
            return apology("You Must Give Money")

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        uptd_cash = user_cash + new_cash

        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)

        return redirect("/")
