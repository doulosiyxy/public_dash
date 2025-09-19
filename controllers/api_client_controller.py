import os
import requests
import functions as fc
import datetime as dt
from utils import db_services as dbs

SAVEIMAGES = True
SAVELOGOS = False

def saveImage(dict: dict, id: str) -> None:
    """
    Saves athlete image file.

    Resquests png url and saves image to images directory. 

        :param dict: image dict containing image url
        :param id: player id
        :type dict: dict
        :type id: str
        :returns: None
        :rtype: None

        :Example: 
        >>> saveImage(
                {
                "href": "https://a.espncdn.com/i/headshots/nfl/players/full/3116726.png",
                "alt": "Kentavius Street"
              },
              "3116726"
        ) 
    """
    
    if SAVEIMAGES:
        if dict != None:
            parameters = "&cquality=80&h=112&w=112&scale=crop&transparent=true"
            url = f"https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/{id}.png{parameters}"
            filepath = f"static/images/{id}.png"
            headers = {}
            if os.path.isfile(filepath):
                lastSavedLocally = fc.convertUnixToRfc(os.path.getmtime(filepath))
                headers = {'If-Modified-Since': lastSavedLocally}
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    dbs.saveImageToDb(response.content, id)
            else: 
                response = requests.get(url)
                if response.status_code == 200:
                    dbs.saveImageToDb(response.content, id)    
        else:
            fc.log(f"{dt.datetime.today()}: {id} no image available.")

def saveLogo(url: str, id: int) -> None:

    """
    Saves large team logo file.

    Requests png url and saves large logo to images directory. 

        :param url: logo url
        :param id: team id
        :type url: str
        :type id: int
        :returns: None
        :rtype: None

        :Example: 
        >>> saveLogo(
            "https://a.espncdn.com/i/teamlogos/nfl/500/atl.png",
            1
        ) 
    """
    if SAVELOGOS:
        response = requests.get(url)
        if response.status_code == 200 :
                dbs.saveLogoToDb(response.content, id)
        else:
            fc.log(f"{dt.datetime.today()}: {id} no logo available.")

def saveSmallLogo(abbr: str, id: int) -> None:
    """
    Saves small team logo file.

    Requests png url and saves small logo to images directory. It ignores NYJ logo.  

        :param abbr: team abbrevation 
        :param id: team id
        :type url: str
        :type id: int
        :returns: None
        :rtype: None

        :Example: 
        >>> saveLogo(
            "ATL",
            1
        ) 
    """
    if SAVELOGOS:
        parameters = "&cquality=80&h=80&w=80"
        url = f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/scoreboard/{abbr}.png{parameters}"
        response = requests.get(url)
        if response.status_code == 200 :
                dbs.saveLogoToDb(response.content, id, "small")
        else:
            fc.log(f"{dt.datetime.today()}: {id} no logo available.")