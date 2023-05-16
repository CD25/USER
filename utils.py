from flask import request
import mysql.connector as conn
import hashlib
import uuid
connection = conn.connect(
    host="localhost",
    user="divy",
    password="divy",
    database="codingthunder",    
)
def fetch_user(username, password):
    cursor = connection.cursor()
    query = "SELECT * FROM USERS WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    row= cursor.fetchone()
    return dict(zip([t[0] for t in cursor.__dict__['_description']], row))


def hash_password(password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + password.encode()).hexdigest()

def checkloginusername():
    username = request.form["username"]
    check = "SELECT * FROM USERS WHERE username=%s OR email=%s OR password=%s"
    if check is None:
        return "No User"
    else:
        return "User exists"
    
def checklogin():
    username = request.form["username"]
    password = request.form["password"]
    query = "SELECT * FROM USERS WHERE username=%s OR email=%s OR password=%s"
    hashpassword = getHashed(password)
    if hashpassword == check["password"]:
        session["username"] = username
        return "correct"
    else:
        return "wrong"
        user = dict(zip([t[0] for t in cursor.__dict__['_description']], row))

class Car:
       attr1="engine"
       attr2 = "tyre"
       def __init__(self,name,engine,tyre):
           self.engine = engine
           self.name = name
           self.tyre = tyre
        engine = Car("V12")
        tyre = Car("Appolo")   
    
    
    msg = ''

# Check if "username" and "password" POST requests exist (user submitted form)
if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    # Create variables for easy access
    username = request.form['username']
    password = request.form['password']

    password = b'password'

    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    # Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, hashed_password))
    # Fetch one record and return result
    account = cursor.fetchone()
    # If account exists in accounts table in our database
    if account:
        # Create session data, we can access this data in other routes
        session['loggedin'] = True
        session['id'] = account['id']
        session['username'] = account['username']
        # Redirect to home page
        return redirect(url_for('home'))
    else:
        # Account doesnt exist or username/password incorrect
        msg = 'Incorrect username/password!'
# Show the login form with message (if any)
return render_template('index.html', msg=msg)



def login():
    error = None
    query = "SELECT username, password FROM USERS"
    # cursor.execute(query)
    if request.method == 'POST':
        username = request.form['username']
        cursor = connection.cursor(DictCursor) # type: ignore
        password = request.form['password']
        password = b'password'
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        query = "SELECT * FROM USERS WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        row= cursor.fetchone()
        user = dict(zip([t[0] for t in cursor.__dict__['_description']], row))
        print("user",user)
        if user:
             # user_dict = dict(zip(columns,row))
            msg = 'Logged in successfully !'
            # print("user", user_dict)
            if user['role'] == 'admin':
                # return render_template('admindashboard.html', error = error, user=user)
                return redirect(url_for('dashboard',username = username, role = user['role']))
            else: 
                print("==================================\n\n\n\n")
                return redirect(url_for("dashboard", username = username, role = user['role']))            
        else:
            error = 'Incorrect username / password !'
    else:    
        
        return render_template('userlogin.html', error = error) 
    