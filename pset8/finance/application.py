import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, validatePassword

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    initialDB_cash = db.execute("SELECT cash FROM users WHERE users.id ==:user_id", user_id = session["user_id"])
    transactions = db.execute("SELECT symbol, SUM(shares) as shares, price  FROM transactions WHERE user_id ==:user_id GROUP BY symbol",
                  user_id = session["user_id"])
    totalDB_price = db.execute("SELECT SUM(price * shares) as total_price FROM transactions WHERE user_id == :user_id",
                    user_id = session["user_id"])

    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares, SUM(price*shares) as total_price FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
            user_id=session["user_id"])
    total_price = 0
    for stock in stocks:
        total_price += stock["total_price"]

    if totalDB_price[0]["total_price"] is None:
        total_price = initialDB_cash[0]["cash"]
    else:
        total_price = initialDB_cash[0]["cash"] - (total_price)

    return render_template(
        "portfolio.html",
        initial_cash = initialDB_cash[0]["cash"],
        transactions = transactions,
        total_price = total_price
        )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("invalid Symbol", 400)
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Please enter positive integer", 400)

        if shares <= 0:
            return apology("Number can not be less than zero", 403)

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
            user_id = session["user_id"],
            symbol = quote["symbol"],
            shares = shares,
            price = quote["price"]
        )
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = :user_id ORDER BY created_at ASC",
        user_id = session["user_id"]
    )
    return render_template("history.html", transactions = transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        usersRow = db.execute("SELECT * FROM users")
        username = request.form.get("username")
        for user in usersRow:
            if user["username"] == username:
                return apology("Current userName already exicts", 403)

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        valPassword = validatePassword(request.form.get("password"))

        if not password:
             return apology("You must confirm a password", 403)
        if confirmation != password:
            return apology("The passwords must coincides", 403)
        if valPassword == -1:
            message = "Password must contain at least 8 points, [A_Z], [a-z], [0-9], [_@$]"
            return render_template("register.html", message=message)

        hashedPassword = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :password)",username=username, password=hashedPassword)
        return redirect("/")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        shares = int(request.form.get("shares"))
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Please enter positive integer", 400)

        if shares <= 0:
            return apology("Number can not be less than zero", 403)

        transactions = db.execute("SELECT * FROM transactions WHERE user_id = :user_id",
            user_id = session["user_id"]
        )

        for transaction in transactions:
            if transaction["symbol"] == quote["symbol"] and transaction["shares"] >= shares:
                db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                    user_id = session["user_id"],
                    symbol = quote["symbol"],
                    shares = -shares,
                    price = quote["price"]
                )

        return redirect("/")
    else:
        translationSymbols = db.execute("SELECT DISTINCT(symbol) FROM transactions WHERE user_id ==:user_id",
            user_id = session["user_id"])
        return render_template("sell.html", translationSymbols = translationSymbols)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)