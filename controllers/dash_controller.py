import functions as fc
from flask import session

def getNextGame():
    session['swapSwitch'] = False
    numberOfGames = len(fc.getThisWeeksGames())
    if session['count'] < numberOfGames - 1:
        session['count'] += 1
        data = fc.getDashboardData(session["user"], session['count'])
        return data
    else: 
        return ('', 204)
    
def getPrevGame():
    session['swapSwitch'] = False
    if session['count'] > 0: 
        session['count'] -= 1
        data = fc.getDashboardData(session["user"], session['count'])
        return data
    else:
        return ('', 204)
    
def swapTeams():
    isSwapped = session['swapSwitch']
    if isSwapped:
        session['swapSwitch'] = False
    else: 
        session['swapSwitch'] = True
    data = fc.getDashboardData(session["user"], session['count'], session['swapSwitch'])
    return data

def refreshDashboard():
    session['swapSwitch'] = False
    data = fc.getDashboardData(session["user"], session['count'], session['swapSwitch'])
    return data

def submitWinner(form):
    team = form.get('teamId')
    game = form.get('gameId')
    if team in fc.TEAMIDS and game in fc.getGameIds(fc.getSeasonYear()):
        return fc.submitAndRespond(team, game, session["user"])
    else:
        return "An error has occurred. Pick not saved. Refresh your browser."

def undoSubmission(form):
    game = form.get('gameId')
    if game in fc.getGameIds(fc.getSeasonYear()):
        return fc.undoPick(game, session["user"])
    else:
        return "An error has occurred. Game not reset. Refresh your browser."