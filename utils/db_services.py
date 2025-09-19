import functions as fc
import datetime as dt
import json

def loadJson(file):
    try:
        with open(file, "r") as f:
            data = json.load(f)
            return data
    except Exception as e:
        pass
        fc.log(f"Error: {e}")

def saveImageToDb(content, id):
    try: 
        with open(f"static/images/{id}.png", "wb") as f:
            f.write(content)
            print(f"{id} image saved successfully")  
    except Exception as e:
            print(f"Error {e}")
            fc.log(f"{dt.datetime.today()}: {e}.")

def saveLogoToDb(content, id, size = ""):
    try: 
        with open(f"static/images/logo{size}{id}.png", "wb") as f:
                f.write(content)
                print(f"{id} {size} logo saved successfully")     
    except Exception as e:
        print(f"Error {e}")
        fc.log(f"{dt.datetime.today()}: {e}.")

def getUserData(user):
     return loadJson("json/db.json")["users"][user]

def getPredictionHistory(user):
     return getUserData(user)["record"]

def getUserNameById(id):
    users = loadJson("json/db.json")["users"]
    for user in users: 
        if users[user]['id'] == id:
            return user 

def getFrndsPredictHist(user):
    record = {}
    friendsList = getUserData(user)['friends']
    for id in friendsList:
        name = getUserNameById(id)
        record[name] = getPredictionHistory(name)
    return record
