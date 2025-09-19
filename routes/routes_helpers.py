from flask import redirect, render_template, session
import auth
import functions as fc
from utils import db_services as dbs

def checkSessionRedirect():
    #session.clear()
    if session.get('loggedIn'):
        return redirect("/dashboard")
    else:
        return render_template("login.html", message="")

def logout():
     session.clear()
     return redirect("/")
    
def authAndLogin(form):
    if session.get("loggedIn"):
        return redirect("/dashboard")
    else: 
        isAuth = isAuth = auth.isUserAuth(form["username"].lower(), form["password"])
        if isAuth:
            return redirect("/dashboard")
        else: 
            return render_template("login.html", message="Invalid email or password")
        
def dashboard():
    if session.get("loggedIn"):
        session['count'] = 0
        data = fc.getDashboardData(session["user"], 0, session['swapSwitch'])
        return render_template('dashboard.html', data=data)
    else:
        return redirect("/")
    
def getFriendHistory():
    user = session["user"]
    data = dbs.getFrndsPredictHist(user)
    record = {}
    for friend in data:
        for year, year_data in reversed(data[friend].items()):
            if year not in record:
                record[year] = {'records': []}
            w = []
            l = []

            for sublist in year_data[1:]:
                for week in sublist:
                    w.append(week[0])
                    l.append(week[1])
            
            total_wins = sum(w)
            total_losses = sum(l)
            percentage = round(total_wins / (total_losses + total_wins) * 100, 2)

            record[year]['records'].append(
                    [friend.title(), total_wins, total_losses, percentage]
                )
            
    print(record)
    return record
    
def history():
    if session.get('loggedIn'):
        user = session["user"]
        data = dbs.getPredictionHistory(user) 
        friends = getFriendHistory()
        record = {}
        for year, year_data in reversed(data.items()):
            w = []
            l = []
            
            for sublist in year_data[1:]:
                for week in sublist:
                    w.append(week[0])
                    l.append(week[1])
            
            total_wins = sum(w)
            total_losses = sum(l)
            percentages = [(w / (w + l)) * 100 for w, l in zip(w, l) if (w + l) != 0]
            percentage = round(total_wins / (total_losses + total_wins) * 100, 2)
            record[year] = {
                "records": [
                    [user.title(), total_wins, total_losses, percentage]
                ],
                "w": w,
                "l": l,
                "percentage": percentages,
                "percent": percentage
            }

            if year in friends and 'records' in friends[year]:
                for friend in friends[year]['records']:
                    record[year]["records"].append(friend)
        
        return render_template("history.html", data=record)
    else:
        return render_template("login.html", message="")
