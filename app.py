import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
import datetime
import logging
FORMAT_LOGGING='%(asctime)s - %(levelname)s - (%(filename)s:%(lineno)d): %(message)s'
logging.basicConfig(level=logging.INFO,format=FORMAT_LOGGING)

DATABASE_FILENAME="/mnt/SSD/Documents/CS50/Week9-FLASK/8-finance/finance.db"
""" FUNCIONES """
def sqlite3_command(command):
    db=sqlite3.connect(DATABASE_FILENAME)
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    try:
        cursor.execute(command)
    except Exception as e:
        logging.error("wrong command [ERROR:{}]".format(e))
        return []
    data=cursor.fetchall()
    db.commit()
    db.close()
    return data

def get_products_and_cash_and_total():
    total=0
    # Obtenemos los productos
    user_id=session["user_id"]
    command="SELECT s.symbol,o.shares,o.price,o.total FROM orders o JOIN stocks s ON s.id=o.symbol_id WHERE user_id={};".format(user_id)
    data=sqlite3_command(command)
    products=[]
    for row in data:
        product={}
        for key in row.keys():
            if key=="price":
                product[key]=usd(row[key])
            elif key=="total":
                total+=row[key]
                product[key]=usd(row[key])
            else:
                product[key]=row[key]
        products.append(product)
    # Obtenemos el cash
    command="SELECT cash FROM users WHERE id={};".format(user_id)
    logging.info(command)
    data=sqlite3_command(command)
    logging.info(data)
    cash=data[0]["cash"]
    total+=cash
    return products,cash,total

def get_quote_price_and_symbol(symbol):
    command="SELECT sale,symbol FROM stocks WHERE LOWER(symbol)=\"{}\";".format(symbol.lower())
    data=sqlite3_command(command)
    if data:
        price=data[0]["sale"]
        new_symbol=data[0]["symbol"]
        return [price,new_symbol]
    return -1

def get_cash_available():
    command="SELECT cash from users WHERE id={}".format(session["user_id"])
    data=sqlite3_command(command)
    return data[0]["cash"]

def get_symbol_id(symbol):
    command="SELECT id FROM stocks WHERE LOWER(symbol)=\"{}\";".format(symbol.lower())
    data=sqlite3_command(command)
    if data:
        symbol_id=data[0]["id"]
        return symbol_id
    return -1

def create_order(symbol,shares,price):
    symbol_id=get_symbol_id(symbol)
    user_id=session["user_id"]
    command="""INSERT INTO orders (
                \"user_id\",
                \"symbol_id\",
                \"shares\",
                \"price\",
                \"total\") VALUES ({},{},{},{},{})""".format(user_id,symbol_id,shares,price,shares*price)
    sqlite3_command(command)
    # Tambien reducimos del cash del usuario
    command="UPDATE users SET cash=cash-{} WHERE id={}".format(shares*price,user_id)
    sqlite3_command(command)

def get_stocks_bought():
    command="SELECT symbol FROM orders o JOIN stocks s ON o.symbol_id=s.id WHERE o.user_id={};".format(session["user_id"])
    data=sqlite3_command(command)
    stocks=[]
    for row in data:
        stock={}
        for key in row.keys():
            stock[ key ] = row[ key ]
        stocks.append(stock)
    return stocks

def get_row_order(symbol):
    command="SELECT * FROM orders o JOIN stocks s ON o.symbol_id=s.id WHERE LOWER(symbol)=\"{}\"".format(symbol.lower())
    logging.info(command)
    data=sqlite3_command(command)
    products=[]
    for row in data:
        product={}
        for key in row.keys():
            product[ key ] = row[key]
        products.append(product)
    return products

def create_transaction(symbol,shares_signed,price):
    symbol_id=get_symbol_id(symbol)
    command="""INSERT INTO transactions (symbol_id, shares, price, date)
                VALUES 
                ({},{},{},\"{}\");""".format(symbol_id,shares_signed,price,datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"))
    sqlite3_command(command)
    return

def get_transactions():
    command="SELECT s.symbol,t.shares,t.price,t.date FROM transactions t JOIN stocks s ON s.id = t.symbol_id;"
    data=sqlite3_command(command)
    transactions=[]
    for row in data:
        transaction={}
        for key in row.keys():
            transaction[key]=row[key]
        transactions.append(transaction)
    return transactions

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
    products,cash,total=get_products_and_cash_and_total()  
    return render_template("index.html", products=products, cash=usd(cash),total=usd(total))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Missing symbol",400)
        if not request.form.get("shares"):
            return apology("Missing amount of shares",400)
        symbol=request.form.get("symbol")
        data=get_quote_price_and_symbol(symbol)
        if data !=-1:
            price,symbol=data[0],data[1]
            shares=request.form.get("shares")
            if shares.isnumeric():
                shares=int(shares)
                ## Verificamos que tengamos monto disponible
                cash_available=get_cash_available()
                if cash_available<price*shares:
                    return apology("cash not available",400)
                products=get_row_order(symbol)
                if products:
                    ## Actualizamos la fila
                    product=products[0]
                    new_shares=product["shares"]+shares
                    new_total=shares*price+product["total"]
                    command="UPDATE orders SET shares={},price={},total={} WHERE id={}".format(new_shares,price,new_total,product["id"])
                    sqlite3_command(command)
                    # Tambien reducimos del cash del usuario
                    command="UPDATE users SET cash=cash-{} WHERE id={}".format(shares*price,session["user_id"])
                    sqlite3_command(command)
                else:
                    ## Creamos la orden del usuario
                    create_order(symbol,shares,price)
                create_transaction(symbol,shares,price)
                flash("Bougth!")
                return redirect("/")

            else:
                return apology("Shares must be numeric",400)
        else:
            return apology("Symbol not found",400)
    return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return render_template("history.html",transactions=get_transactions())

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
        command="SELECT * FROM users WHERE username = \"{}\"".format(request.form.get("username"))
        data = sqlite3_command(command)
        # Ensure username exists and password is correct
        if len(data) != 1 or not check_password_hash(data[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = data[0]["id"]

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
        symbol=request.form.get("symbol")
        data=get_quote_price_and_symbol(symbol)
        if data!=-1:
            price,symbol=data[0],data[1]
            return render_template("quote.html",symbol=symbol,price=usd(price))
        else:
            return apology("Invalid Symbol",400)
        
    return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    msg = "Please register with an username and password"
    if request.method == "POST":
        """Register user"""
        # verificamos que tenga usuario
        if not request.form.get("username"):
            msg="Please provide an USERNAME"
        # verificamos que tenga password
        elif not request.form.get("password"):
            msg="Please provide a PASSWORD"
        elif not request.form.get("re-password"):
            msg="Please re-enter the PASSWORD"
        elif request.form.get("password")!=request.form.get("re-password"):
            msg="PASSWORD is not equal"
        else:
            # Registramos el usuario
            username=request.form.get("username")
            hash = generate_password_hash(request.form.get("password"))
            command="INSERT INTO users (username, hash) VALUES (\"{}\", \"{}\")".format(username,hash)
            logging.info("sending sqlite3 command: {}".format(command))
            sqlite3_command(command)
            return redirect("/login")
    ## Caso del GET
    flash(msg)
    return render_template("register.html")
        
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Verificamos que recibimos un symbolo correcto
        if not request.form.get("symbol"):
            return apology("Symbol not selected")
        symbol=request.form.get("symbol")
        data=get_quote_price_and_symbol(symbol)
        if data==-1:
            return apology("Symbol not found")
        price,symbol=data[0],data[1]
        # Verificamos que recibimos un share adecuado
        if not request.form.get("shares"):
            return apology("Shares not selected")
        shares=request.form.get("shares")
        if not shares.isnumeric():
            return apology("Shares is not numeric!")
        shares=int(shares)
        ## hallamos el id de la orden para hallar la cantidad de shares
        products=get_row_order(symbol)
        product=products[0]
        if shares<=0 or shares>product["shares"]:        
            return apology("Select a correct amount of shares")
        ## Actualizamos el cash del cliente
        user_id=session["user_id"]
        sell_amount=price*shares
        command="UPDATE users SET cash=cash+{} WHERE id={}".format(sell_amount,user_id)
        sqlite3_command(command)
        ## Actualizamos el shares, Si es igual a la cantidad maxima, eliminamos fila.
        symbol_id=get_symbol_id(symbol)
        if shares==product["shares"]:
            # Eliminamos la fila de la orden
            command="DELETE FROM orders WHERE symbol_id={}".format(symbol_id)
        else:
            # Modificamos la fila de la orden
            new_shares=product["shares"]-shares
            command="UPDATE orders SET shares={},total={} WHERE symbol_id={}".format(new_shares,new_shares*price,symbol_id)
        sqlite3_command(command)
        create_transaction(symbol,-shares,price)
        flash("Sold!")
        return redirect('/')
    ## GET: Buscamos los symbolos que ya se tienen
    stocks = get_stocks_bought()
    return render_template("sell.html",stocks=stocks)
