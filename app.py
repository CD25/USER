import MySQLdb
import bcrypt
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector as conn

from MySQLdb.cursors import DictCursor
from enum import Enum

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://divy:divy:@localhost/codingthunder"
app.secret_key = "secret-key"

# MySQL database configuration
connection = conn.connect(
    host="localhost",
    user="divy",
    password="divy",
    database="codingthunder",
)
db = SQLAlchemy(app)


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


class USERS(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.USER)

    cursor = connection.cursor(DictCursor)  # type: ignore


@app.route("/", methods=["GET", "POST"])
def home():
    return redirect(url_for("dashboard"))


# -------------------------------------------------------------------------------------


@app.route("/login", methods=["GET", "POST"])
def login():
    # error = None

    if request.method == "POST":
        cursor = connection.cursor(DictCursor)  # type: ignore

        username = request.form["username"]

        password = request.form["password"]

        cursor.execute("SELECT * FROM USERS WHERE username = %s ", (username,))
        row = cursor.fetchone()
        if row:
            user = dict(zip([t[0] for t in cursor.__dict__["_description"]], row))  # type: ignore

            # user = cursor.fetchone()
            print("user", user)
            if user:
                print("yyyyyyyyye")

                hashed_password = user["password"]
                check_status = bcrypt.checkpw(
                    password.encode("utf-8"), hashed_password.encode("utf-8")
                )
                print("check status", check_status)
                if check_status is True:
                    print("Valid Login Credentials")
                    session["loggedin"] = True
                    session["user"] = user  # type: ignore
                    print("user", user["role"])
                    return redirect(url_for("dashboard"))
                else:
                    print("nooo")
                    error = "Incorrect username / password !"
                    return render_template("userlogin.html", error=error)
            else:
                print("qqqq")
                error = "Incorrect username / password !"
                return render_template("userlogin.html", error=error)
        else:
            error = "Incorrect username / password !"
            return render_template("userlogin.html", error=error)

    else:
        return render_template("userlogin.html")


# -------------------------------------------------------------------------------------


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user" in session:
        user = session["user"]
        if user["role"] == "admin":
            return render_template("admindashboard.html", user=user)
        else:
            return render_template("userdashboard.html", user=user)
    else:
        return render_template("userlogin.html")


# -------------------------------------------------------------------------------------


@app.route("/signup", methods=["GET", "POST"])
def signup():
    cursor = connection.cursor()
    # print("-------", (request.form).to_dict(flat=False))
    if request.method == "POST":
        data = (request.form).to_dict(flat=False)
        print("DATA: ", data)
        username = data["username"][0]
        password = data["password"][0]
        # password = b'password'
        password = bytes(password, "utf-8")
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        email = data["email"][0]
        print("USERNAME", username)
        print("hererererererer-1111")
        # requestJson = request.get_json(force=True)
        print("hererererererer-8989898989")
        query = "SELECT * FROM USERS WHERE username=%s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        if user:
            print("User already Exists.")
            error = "Username already Exists. Please enter another username"
            return render_template("usersignup.html", error=error)
        else:
            print("ELSEEEE")
            try:
                print("try")
                query = (
                    "INSERT INTO USERS (username, password, email) VALUES (%s,%s,%s)"
                )
                cursor.execute(query, (username, hashed_password, email))
                connection.commit()
            except Exception as e:
                print("except")
                print("ERRO is: ", e)
            return render_template("userlogin.html")
    else:
        print("hererererererer---222")
        return render_template("usersignup.html")


# -------------------------------------------------------------------------------------

import json


@app.route("/api/users", methods=["GET"])
def get_users():
    print("gfds")
    cursor = connection.cursor(dictionary=True)  # type: ignore
    query = "SELECT * FROM USERS"
    cursor.execute(query)
    # return jsonify({"user": json.loads(users.data)})

    # Fetch all the rows as a list of tuples
    users = cursor.fetchall()
    # Create a dictionary with user information
    result = []
    for user in users:
        username = (user["username"],)  # type: ignore
        password = (user["password"],)  # type: ignore
        email = (user["email"],)  # type: ignore
        role = user["role"]  # type: ignore
        result.append(
            {"username": username, "password": password, "email": email, "role": role}
        )

    return jsonify(result)


@app.route("/users", methods=["GET", "POST"])
def users():
    # cursor = connection.cursor(DictCursor)
    # query = "SELECT * FROM USERS"
    # cursor.execute(query)
    # cursor.fetchall()
    # print(users)
    cursor = connection.cursor(dictionary=True)  # type: ignore
    query = "SELECT * FROM USERS"
    cursor.execute(query)

    # Fetch all the rows as a list of tuples
    users = cursor.fetchall()
    users = jsonify(users)
    import json

    # return jsonify({"user": json.loads(users.data)})
    return render_template("users.html", user=users)

    # cursor = connection.cursor(DictCursor)
    # cursor.execute("SELECT * FROM USERS")
    # row = cursor.fetchall()
    # user = dict(zip([t[0] for t in cursor.__dict__["_description"]], row))
    # print("Users are:", user)
    # return user


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user", None)
    return redirect("/")


@app.route("/city", methods=["GET"])
def cities_page():
    return render_template("countries.html")


@app.route("/api/city/<state_id>", methods=["GET"])
def city(state_id):
    cursor = connection.cursor()
    query = "SELECT * FROM cities WHERE state_id=%s"
    cities = cursor.execute(query, (state_id,))
    rows = cursor.fetchall()
    list = []
    for row in rows:
        cities = dict(zip([t[0] for t in cursor.__dict__["_description"]], row))
        list.append(cities)
    # countries = jsonify(countries)
    print("cities", list)
    return list


@app.route("/state", methods=["GET"])
def states_page():
    return render_template("countries.html")


@app.route("/api/state/<country_id>", methods=["GET"])
def state(country_id):
    cursor = connection.cursor()
    query = "SELECT * FROM states WHERE country_id=%s"
    states = cursor.execute(query, (country_id,))
    rows = cursor.fetchall()
    list = []
    for row in rows:
        states = dict(zip([t[0] for t in cursor.__dict__["_description"]], row))
        list.append(states)
    # countries = jsonify(countries)
    print("states", list)
    return list


@app.route("/country", methods=["GET"])
def country_page():
    return render_template("countries.html")


@app.route("/api/country", methods=["GET"])
def country():
    # country = request.form['country']
    # country = "India"
    cursor = connection.cursor()
    query = "SELECT * FROM country"
    countries = cursor.execute(query)
    rows = cursor.fetchall()
    lst = []
    for row in rows:
        countries = dict(zip([t[0] for t in cursor.__dict__["_description"]], row))
        lst.append(countries)
    # countries = jsonify(countries)
    
    return lst
    # return render_template("countries.html", country=country)


if __name__ == "__main__":
    app.run(debug=True)
    
    
    
                