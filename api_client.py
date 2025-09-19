#source: https://gist.github.com/nntrn/ee26cb2a0716de0947a0a4e9a157bc1c

import os
import requests
import functions as fc
import datetime as dt
from utils import api_client_helpers as ach
from controllers import api_client_controller as acc
#from flask_apscheduler import APScheduler

#This variable needs to be set by a unique function that 
# gets current year by condition of where we are in season
# not with fc.getSeasonYear()
season = 2025 

#scheduler = APScheduler()

SAVEIMAGES = True
SAVELOGOS = False

def getNews(team: int) -> list[list]:
    """
    Gets news articles by team.

    Requests team news API and returns list of articles. Responds with JSON.

        :param team: team id
        :type team: int
        :returns: newsList
        :rtype: list[list]

        :Example: 
        >>> getNews(1) 
        [
            [
                "d3682b22ed39f",
                "static/images/logosmall19.png",
                "Giants QB Drew Lock has heel injury; Tommy DeVito to start",
                "The Giants are expected to start Tommy DeVito at quarterback vs. the Ravens on Sunday while Drew Lock, who started the past two games, recovers from a heel injury.",
                "https://www.espn.com/nfl/story/_/id/42913640/giants-qb-drew-lock-heel-injury-tommy-devito-start",
                19
            ]
        ]
    """
    newsList = []
    url = ach.getEndpoint('teamNews').format(team)
    response = requests.get(url)
    try: 
        if response.status_code == 200:
            print("News request successful...")
            data = response.json()['articles']
            for article in data:
                if fc.isRelevantNews(article, team):
                    list = [
                            article.get('dataSourceIdentifier'),
                            f"static/images/logosmall{team}.png",
                            article.get('headline'),
                            article.get('description'),
                            article.get('links')['web']['href'],
                            team
                        ]
                    newsList.append(list)
        return newsList    
    except:
        fc.log(f"{dt.datetime.today()}: {id} news request unsuccessful.")  
        return ["No news available", "Comeback later for updates. Or visit EPSN.", ""]               
   
def getCalendar(year: int, week: int, seasontype: int) -> list[dict]:
    
    """
    Gets NFL full year calender.

    Requests schedule API to return week details by year, week and season type. 
    Week and season type are set to 1, as full calender is available in each type.

        :param year: season year
        :param week: week
        :param seasontype: season type i.e. pre, regular etc. 
        :type year: int
        :type week: int
        :type seasontype: int
        :returns: weeks
        :rtype: list[dict]

        :Example: 
        >>> getCalendar(2024, 1, 1) 
        [
            {
                "name": "Week 1",
                "shortName": "Week 1",
                "start": "2025-02-15T08:00Z",
                "end": "2025-08-01T06:59Z",
                "detail": "Feb 15-Jul 31",
                "value": "1"
            }
        ]

    """
    
    url = ach.getEndpoint("schedule").format(year, week, seasontype)
    response = requests.get(url)
    weeks = []
    if response.status_code == 200:
        print("Calender request successful...")
        data = response.json()
        events = data["content"]['calendar']
        for event in events:
            for week in event["entries"]:
                week = {
                    "name": week.get('label'),
                    "shortName": week.get('alternateLabel'),
                    "start": week.get('startDate'),
                    "end": week.get('endDate'),
                    "detail": week.get('detail'),
                    "value": week.get('value')
                }
                weeks.append(week)
        return weeks
    else:
        fc.log(f"{dt.datetime.today()}: calender request failed.")

def getSeasonData() -> dict[dict]:
    """
    Gets all four season type data.

    Requests season API to return dict of starts
    and ends of each season type: pre, regular, post, off.

        :returns: seasonDict
        :rtype: dict[dict]

        :Example: 
        >>> getSeasonData()
        {
            "year": 2024,
            "pre": {
                "id": "1",
                "name": "Preseason",
                "startDate": "2024-08-01T07:00Z",
                "endDate": "2024-09-05T06:59Z"
            }
        }

    """
    url = ach.getEndpoint("season").format(season)
    response = requests.get(url)
    data = {}
    if response.status_code == 200:
        print("Season data retrieved.")
        data = response.json().get('types')['items']
        seasonDict = {
            "year": season,
            "pre": {
                "id": data[0].get('id'),
                "name": data[0].get('name'),
                "startDate": data[0].get('startDate'),
                "endDate": data[0].get('endDate')
            },
            "regular": {
                "id": data[1].get('id'),
                "name": data[1].get('name'),
                "startDate": data[1].get('startDate'),
                "endDate": data[1].get('endDate') 
            },
            "post": {
                "id": data[2].get('id'),
                "name": data[2].get('name'),
                "startDate": data[2].get('startDate'),
                "endDate": data[2].get('endDate') 
            },
            "off": {
                "id": data[3].get('id'),
                "name": data[3].get('name'),
                "startDate": data[3].get('startDate'),
                "endDate": data[3].get('endDate')
            }  
        }
        return seasonDict
    else:
        fc.log(f"{dt.datetime.today()}: season request failed.")

def getProjections(teamId: int) -> dict:
    """
    Gets projections by team id.

    Requests projections API to return dict of projections each week.

        :param teamId: team id
        :type teamId: int
        :returns: projections
        :rtype: dict

        :Example: 
        >>> getProjections(19)
        {
            "chanceToWinThisWeek": 0.18540999999999996,
            "chanceToWinDivision": 0.0,
            "projectedWins": 3.022,
            "projectedLosses": 13.928
        }

    """
    if fc.isInSeason():
        url = ach.getEndpoint("projections").format(fc.getSeasonYear(), teamId)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            projections = {
                "chanceToWinThisWeek": data.get("chanceToWinThisWeek"),
                "chanceToWinDivision": data.get("chanceToWinDivision"),
                "projectedWins": data.get("projectedWins"),
                "projectedLosses": data.get("projectedLosses")
            }
            return projections
    else: 
        return {}

def getSchedule(year: int, week: int, seasontype: int) -> list[list[dict]]:

    """
    Gets season game schedule.

    Requests schedule API to return list of games per seasontype for the whole season.

        :param year: season year
        :param week: season year
        :param seasontype: season year
        :type year: int
        :type week: int
        :type seasontype: int
        :returns: games
        :rtype: list[list[dict]]

        :Example: 
        >>> getSchedule(2024, 1, 1)
        [
            [...hall of fame week],
            [...preseason week 1],
            [...preseason week 2],
            [...preseason week 3
                {game 1},
                {game 2}
            ]
        ]

        i.e. 

        [
            [
                {
                    "gameid": "401671610",
                    "name": "Houston Texans at Chicago Bears",
                    "shortName": "HOU VS CHI",
                    "homeTeamId": "3",
                    "awayTeamId": "34",
                    "date": "2024-08-02T00:00Z",
                    "status": {
                    "period": 3,
                    "displayClock": "3:31",
                    "clock": 211,
                    "type": {
                        "name": "STATUS_FINAL",
                        "description": "Final",
                        "id": "3",
                        "state": "post",
                        "completed": true,
                        "detail": "Final",
                        "shortDetail": "Final"
                    }
                    },
                    "winner": "3",
                    "score": "17-21",
                    "seasontype": 1,
                    "week": 1,
                    "headline": null,
                    "weekName": "Hall of Fame Weekend",
                    "weather": null
                }
            ]
        ]

    """

    url = ach.getEndpoint("schedule").format(year, week, seasontype)
    response = requests.get(url)
    if response.status_code == 200:
        print("Schedule request successful...")
        data = response.json()
        dates = data["content"]['schedule']
        games = []
        gameDict = {}
        for date in dates:
            gameList = dates[date]["games"]
            for game in gameList:
                headline = None
                fc.storeGameId(game['competitions'][0]['id'], year)
                if seasontype == 3:
                    headline = game['competitions'][0]['notes'][0]['headline']
                gameDict = {
                    "gameid": game['competitions'][0]['id'],
                    "name": game.get("name"),
                    "shortName": game.get("shortName"),
                    "homeTeamId": game['competitions'][0]["competitors"][0]["id"],
                    "awayTeamId": game['competitions'][0]["competitors"][1]["id"],
                    "date": game.get("date"),
                    "status": game.get("status"),
                    "winner": fc.getWinners(game),
                    "score": fc.getScores(game),
                    "seasontype": seasontype,
                    "week": week,
                    "headline": headline,
                    "weekName": fc.getWeek(game["date"]),
                    "weather": {
                        "description": game.get('weather')['displayValue'],
                        "id": game.get('weather')['conditionId'],
                        "temp": str(game.get('weather')['temperature'])
                    } if game.get('weather') else None
                }
                games.append(gameDict)
                #print(f"{gameDict['shortName']} added")     
        return games
    else:
        print("Schedule request unsuccessful")
        fc.log(f"{dt.datetime.today()}: schedule request failed.")

def getTeamData(id: int) -> dict:
    """
    Gets team data by team id.

    Requests team API to return dict containing data for the team.

        :param teamId: team id
        :type teamId: int
        :returns: team
        :rtype: dict

        :Example: 
        >>> getTeamData(19)
        {
            "id": str,
            "slug": str,
            "location": str,
            "name": str,
            "nickname": str,
            "abbreviation": str,
            "displayName": str,
            "shortDisplayName": str,
            "color": str,
            "alternateColor": str,
            "logos": str,
            "record": str,
            "standingSummary": str,
            "defForm": str,
            "offForm": str,
            "projections": dict,
            "standings": list,
            "news": list[list]
        }

    """

    url = ach.getEndpoint("teams").format(id)
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Team {id} data request successful...")
        data = response.json()["team"]
        if id != 20:
            acc.saveLogo(data.get("logos")[0]["href"], id)
            acc.saveSmallLogo(data.get("abbreviation"), id)

        team = {
            "id": data.get("id"),
            "slug": data.get("slug"),
            "location": data.get("location"),
            "name": data.get("name"),
            "nickname": data.get("nickname"),
            "abbreviation": data.get("abbreviation"),
            "displayName": data.get("displayName"),
            "shortDisplayName": data.get("shortDisplayName"),
            "color": data.get("color"),
            "alternateColor": data.get("alternateColor"),
            "logos": data.get("logos")[0]["href"],
            "record": data.get("record")["items"][0]["summary"] if data.get("record") else '0-0',
            "standingSummary": data.get('standingSummary'),
            "defForm": "",
            "offForm": "",
            "projections": getProjections(id),
            "standings": [],
            "news": getNews(id)
        }
    
        return team
    else:
        fc.log(f"{dt.datetime.today()}: team {id} request failed.")
        

def getAthleteStats(rank: any, url: str) -> dict:

    """
    Gets athlete data by rank from athlete url.

    Requests athlete stats API to return dict containing data for that athlete.

        :param rank: athlete rank
        :type rank: any
        :param url: athlete stats url
        :type url: str
        :returns: athleteDict
        :rtype: dict

        :Example: 
        >>> getAthleteStats(1, "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/positions/31?lang=en&region=us")
        {
            "id": str,
            "rank": int,
            "href": str,
            "fullName": str,
            "shortName": str,
            "displayWeight": str,
            "height": float,
            "displayHeight": str,
            "age": int,
            "jersey": str,
            "position": dict,
            "injuries": list,
            "statistics": dict,
            "active": boolean,
            "experience" : dict,
            "headshot": dict
        }

    """
    
    response = requests.get(url)
    if response.status_code == 200:
        print(f"{response.status_code}: request suceeded...")
        data = response.json()
        acc.saveImage(data.get('headshot'), data.get('id'))
        athleteDict = {
            "id": data.get('id'),
            "rank": rank,
            "href": url,
            "fullName": data.get('fullName'),
            "shortName": data.get('shortName'),
            "displayWeight": data.get('displayWeight'),
            "height": data.get('height'),
            "displayHeight": data.get('displayHeight'),
            "age": data.get('age'),
            "jersey": data.get('jersey'),
            "position": data.get("position"),
            "injuries": data.get('injuries'),
            "statistics": data.get('statistics'),
            "active": data.get('active'),
            "experience" : data.get('experience'),
            "headshot": data.get('headshot')
        }
        print(f"Fetching {data.get('fullName')}...")
        print(f"{data.get('fullName')} added.")
        return athleteDict
    else: 
        #print(f"{response.status_code}: request failed")
        fc.log(f"{dt.datetime.today()}: {data.get('fullName')} request failed.")
    
def getDepthCharts(year: int, teamId: int) -> dict:

    """
    Gets season depthcharts for team by team id.

    Requests team depthchart API to get each position's athletes. 
    Calls getAthleteStats() for each athlete in each position 
    to add basic stats to dict.

    :param year: season year
    :param teamId: team id
    :type year: int
    :type teamId: int
    :returns: depthChartDict
    :rtype: dict

    :example:
    >>> getDepthCharts(2024, 1)

    {
        "ATL": {
            "LDE": {
            "name": "Left Defensive End",
            "athletes": [
                {
                "id": "2576492",
                "rank": 1,
                "href": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/athletes/2576492?lang=en&region=us",
                "fullName": "Grady Jarrett",
                "shortName": "G. Jarrett",
                "displayWeight": "288 lbs",
                "height": 72.0,
                "displayHeight": "6' 0\"",
                "age": 31,
                "jersey": "97",
                "position": {
                    "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/positions/31?lang=en&region=us",
                    "id": "31",
                    "name": "Defensive End",
                    "displayName": "Defensive End",
                    "abbreviation": "DE",
                    "leaf": false,
                    "parent": {
                    "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/positions/71?lang=en&region=us"
                    }
                },
                ...athletes
                ],
                ...position
            }
        }
    }
    
    """

    url = ach.getEndpoint("depthchart").format(year, teamId)
    response = requests.get(url)
    if response.status_code == 200:
        print(f"{dt.datetime.today()}: Depth chart request successful.")
        data = response.json()
        itemsList = data.get('items')
        teamName = fc.getAbbreviationById(teamId)
        print(teamName)
        depthChartDict = {}
        formations = []
        for item in itemsList:
            formations.append(item.get('name'))
            #the following could be another function.
            for position in item.get("positions"):
                athleteList = []
                subposition = item.get('positions')[position]
                depthChartDict[f"{position.upper()}"] = {
                    "name": f"{subposition.get('position')['name']}",
                }
                for athlete in subposition.get('athletes'):
                    athleteList.append(getAthleteStats(athlete.get('rank'), athlete['athlete'].get('$ref')))
                    depthChartDict[f"{position.upper()}"]["athletes"] = athleteList    
        depthChartDict['formations'] = formations
        return {f"{teamName}": depthChartDict}
    else: 
        fc.log(f"{dt.datetime.today()}: Depth chart request unsuccessful.")
    
def getStandings(conference: int, division: int, team: int) -> dict:

    """
    Gets standing data for each conference and division.

    Requests standings API.

    :param conference: conference id
    :param division: division id
    :param team: team id
    :type conference: int
    :type division: int
    :type team: int
    :returns: standing
    :rtype: dict

    :example:
    >>> getStandings(1, 1, 1)

        {
          "id": "1",
          "seed": "9",
          "stats": [
            "6", #wins
            "7", #losses
            "0", #ties
            ".462", #pct.
            "4-3", #home
            "2-4", #away
            "3-2", #div
            "5-4", #conference
            "264", #points for
            "292", #points against
            "-28", #points difference
            "W1" #streak
          ]
        }

    """

    url = ach.getEndpoint('standings')
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        entry = data['content']['standings']['groups'][conference]['groups'][division]['standings']['entries'][team]
        team = entry['team']
        stats = entry['stats']
        standing = {
            "id" : team.get('id'),
            "seed" :team.get('seed'),
            "stats" : [stat['displayValue'] for stat in stats]
        }
        return standing
    else: 
        print("standings unsuccessful")
        fc.log(f"{dt.datetime.today()}: Standings request unsuccessful.")


def getAthleteFullStats():
    url = "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/athletes/3126486/statistics?lang=en&region=us"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        stats = data.get('splits')['categories']
        athleteStatsDict = {}
        for list in stats:
            print(list['name'].upper())
            for dict in list['stats']:
                rank = dict.get('rank')
                if not dict['value'] == 0:
                    if rank != None and rank in range(1, 31):
                        print(f"{dict['name']}: {round(dict['value'])}: {rank}")
    else: 
        print("Full stats unsuccessful")
        fc.log(f"{dt.datetime.today()}: Full stats request unsuccessful.")

#@scheduler.task('cron', id='season', year="*", month=8, day=1, misfire_grace_time=900, timezone='Europe/London')
def refreshSeasonData() -> None:

    """
    Refreshes season data.

    Calls getSeasonData() stores dict to g.json. 
    Logs to log.txt.

    cron shedule: every year, 1st August.
    """

    try: 
        seasonDict = getSeasonData()
        fc.storeData("season", seasonDict, "json/g.json")
        fc.log(f"{dt.datetime.today()}: Season data saved.")
    except Exception as e:
        fc.log(f"{dt.datetime.today()}: {e}")

#@scheduler.task('cron', id='schedule', day_of_week='thu-tue', hour = 5, minute = 2, misfire_grace_time = 900, timezone='Europe/London')    
def refreshSchedule() -> None:

    """
    Refreshes schedule data.

    Loops through each seasontype id (1-4) & gets weeks for each seasontype.
    Loops through each week & appends each game to games list.
    Saves games list to g.json.
    Logs to log.txt.

    cron shedule: thurs to tues, 05:02 am.
    """

    games = []
    seasontype = 0
    for i in range(1, 4):
        file = "json/g.json"
        seasontype = i
        weeks = fc.getWeeks(seasontype)
        print(f"Season type: {seasontype}")
        for j in range(1, weeks + 1):
            try: 
                games.append(getSchedule(season, j, seasontype))
            except Exception as e:
                fc.log(f"{dt.datetime.today()}: {e}")
                continue
    try:
        fc.storeData("games", games, file)
        fc.log(f"{dt.datetime.today()}: Schedule saved.")
    except Exception as e:
        fc.log(f"{dt.datetime.today()}: {e}")

#@scheduler.task('cron', id='dchart', day_of_week='mon-sun', hour = 5, minute = 0, misfire_grace_time = 900, timezone='Europe/London')    
def refreshTeamData() -> None:

    """
    Refreshes team data.

    Loops through each team id (1-35 ignoring 31 & 32) & appends returned dict to teams list.
    Saves teams list to t.json.
    Logs to log.txt.

    cron shedule: mon to sun, 05:00am.
    """

    teams = []
    for i in range(1, 35):
        try: 
            if i == 31 or i == 32:
                continue
            teams.append(getTeamData(i))
            
        except Exception as e:
            fc.log(f"{dt.datetime.today()}: {e}")
            continue
    fc.storeData("teams", teams, "json/t.json")
    fc.log(f"{dt.datetime.today()}: Team data saved.")

#@scheduler.task('cron', id='dchart', day_of_week='mon-sun', hour = 5, minute = 5, misfire_grace_time = 900, timezone='Europe/London')
def refreshDepthChartData() -> None:
     
    """
    Refreshes depth chart data.

    Loops through each team id in list of teams playing this week & appends returned dict to depthchart list.
    Saves depthchart list to dchart.json.
    Logs to log.txt.

    cron shedule: mon to sun, 05:05am.
    """
    import time
    startTime = time.time()
    print(startTime)
    depthCharts = []

    if fc.isInSeason():
        teamIDList = fc.getThisWeeksTeamIDs()
        for teamID in teamIDList:
            try:
                depthCharts.append(getDepthCharts(season, int(teamID)))
            except Exception as e:
                fc.log(f"{dt.datetime.today()}: {e}")
                continue
        endTime = time.time()
        print(f"{(endTime - startTime) / 60} minutes to request all depthcharts.")
    else:
        for i in range(1, 35):
            try:
                if i == 31 or i == 32:
                    continue
                depthCharts.append(getDepthCharts(season, i))
            except Exception as e:
                fc.log(f"{dt.datetime.today()}: {e}")
                continue
    fc.storeData("depthCharts", depthCharts, "json/dchart.json")
    fc.log(f"{dt.datetime.today()}: Depth chart data saved.")

#@scheduler.task('cron', id='weeks', year="*", month=8, day=1, hour = 5, minute = 3, misfire_grace_time = 900, timezone='Europe/London')
def refreshWeekData() -> None:
    """
    Refreshes week data.

    Calls getCalendar() for dict of games by week.
    Appends week games dict to weeks list.
    Saves week list to g.json.
    Logs to log.txt.

    cron shedule: every year, 1st August, 05:03am
    """
    weeks = []
    try:
        weeks = getCalendar(fc.getSeasonYear(), 1, 1)
        fc.storeData("weeks", weeks, "json/g.json")
        fc.log(f"{dt.datetime.today()}: Weeks saved")
    except Exception as e:
        fc.log(f"{dt.datetime.today()}: {e}")

#@scheduler.task('cron', id='standings', day_of_week='tue', hour = 5, minute = 40, misfire_grace_time = 900, timezone='Europe/London')
def refreshStandings() -> None:
    """
    Refreshes standings data.

    Loops through each conference. 
    Then loops through each division in each conference, initialising list for each division, in standings dict.
    Then loops through each team in each division, calling getStandings() for each team.
    Appends each team standing to division list in each standings conference.
    Saves standings dict to st.json.
    Logs to log.txt.

    cron shedule: every tues, 05:40am
    """
    
    conName = {
        0: "AFC",
        1: "NFC"
    }
    divName = {
        0: "East",
        1: "North",
        2: "South",
        3: "West"
    }
    standings = {
        "AFC": {

        },
        "NFC": {

        }
    }
    for con in range(2):
            for div in range(4):
                print("requesting", conName[con], divName[div] + "...")
                standings[conName[con]][divName[div]] = []
                for team in range(4):
                    try:
                        standing = getStandings(con, div, team)
                        standings[conName[con]][divName[div]].append(standing)
                    except Exception as e:
                        fc.log(f"{dt.datetime.today()}: {e}")
                        continue
    print("Standing request complete.")
    fc.storeData("standings", standings, "json/st.json")
    print("Standing data saved.")
    fc.log(f"{dt.datetime.today()}: Standings saved")

#@scheduler.task('cron', id='schedule', day_of_week='thu-tue', hour = 5, minute = 30, misfire_grace_time = 900, timezone='Europe/London')
def refreshUserRecords() -> None:
    """
    Refreshes all user records.

    Before calculating records missing record and pick years and weeks are added.
    
    Logs to log.txt.

    cron shedule: thurs to tues, 05:30am
    """
    try:
        weekValue = int(fc.getWeekValue())
        season = str(fc.getSeasonYear())
        seasonType = int(fc.getSeasonType())
        usernames = fc.getUsernames()
        for user in usernames:
            record = fc.calculateRecords(season, user)
            fc.updateRecord(record, user, season, seasonType, weekValue)
        print("Records updated")
        fc.log(f"{dt.datetime.today()}: Records updated.")
    except Exception as e:
        print("error", e)
        fc.log(f"{dt.datetime.today()}: {e}")

'''#refreshSeasonData()
refreshSchedule()
refreshTeamData()
refreshDepthChartData()
#refreshWeekData()
refreshStandings()
refreshUserRecords()'''