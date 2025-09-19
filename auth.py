import functions as fc
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

def isUserAuth(username, password):
    users = fc.loadJson("json/db.json")["users"]
    if username not in users:
         return False
    
    password_hash = users[username]['password']
    print(password_hash)
    if check_password(password_hash, password):
        setSession(users[username]['id'], username)
        return True  
    else: 
        return False

def setSession(id, username):
    session["loggedIn"] = id #users[user]["id"]
    session["user"] = username
    session['swapSwitch'] = False

def set_password(password):
    return generate_password_hash(password)

def check_password(password_hash, password):
    return check_password_hash(password_hash, password)
