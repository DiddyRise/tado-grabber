#!/bin/python3

#big thank you to this guide --> https://shkspr.mobi/blog/2019/02/tado-api-guide-updated-for-2019/ <-- for explaining the API

from time import sleep
from urllib import response
import requests
import datetime
import json
from file_handler import createLog
import os
import random

#------ login variables
username = "" # your tado login 
password = "" # your tado password
client_secret = "" # your tado client secret

#------- getHistory() variables - Use for single log downloads
date = datetime.date(2022,4,1)
singleZoneID = "3"

#------------------ getHistoryRange() - Use these variables if you want to download all logfiles from all zones for a certain timeframe
start_date = datetime.date(2022,5,1) # First date to check for logs
end_date = datetime.date(2022,5,2) # Last date to check for logs
zoneCount = 5 # How many zones (Rooms) do you have? 

#------------------------------------------
# get information about your zones
def getZones():
    r=requests.get("https://my.tado.com/api/v2/homes/" + homeId + "/zones", headers={"Authorization" : "Bearer" + bearerToken})
    response = json.loads(r.text)
    for zones in response:
        print(str(zones["id"]) + ": " + zones["name"])
    
    # print(json.dumps(response, indent=1))

#get historical information based on a date range
def getHistoryRange():
    zone_list = list(range(1, zoneCount+1)) # creates a list of zones based on the zoneCount variable
    zone_names = []
    
    r=requests.get("https://my.tado.com/api/v2/homes/" + homeId + "/zones", headers={"Authorization" : "Bearer" + bearerToken})
    response = json.loads(r.text)
    zone_i = 0
    for zones in response:
        zone_names.append(zones["name"])

    
    date_list = [] # creates a list of dates based on the start_date and end_date variable
    diff = end_date - start_date
    for i in range(diff.days + 1):
        date = (start_date + datetime.timedelta(i))
        date_list.append(date)
    
    for zoneID in zone_list:
        zoneID = str(zoneID)
        zoneName = zone_names[zone_i]

        for date in date_list:
            date = str(date)

            r=requests.get("https://my.tado.com/api/v2/homes/" + homeId + "/zones/" + zoneID + "/dayReport?date=" + date, headers={"Authorization" : "Bearer" + bearerToken})
            response = json.loads(r.text)
                        
            logname = date + "_" + zoneName
            
            path = (date + "/")
            if not os.path.exists(path):
                os.makedirs(path)
            
            f=open(date + "/" + logname + ".json", "w")
            f.write(json.dumps(response, indent=1))
            f.close
                      
            print("Downloaded: " + logname)
            
            createLog(path, logname)
            sleep(random.randint(0, 3)) #you can disable this if you want faster downloads - just keep in mind that you might overload the TADO API and lock youself out.
        
        zone_i = zone_i + 1

#get historical information based on the date variable
def getHistory():

    zone_names = []
    
    r=requests.get("https://my.tado.com/api/v2/homes/" + homeId + "/zones", headers={"Authorization" : "Bearer" + bearerToken})
    response = json.loads(r.text)
    for zones in response:
        zone_names.append(zones["name"])
    
    r=requests.get("https://my.tado.com/api/v2/homes/" + homeId + "/zones/" + singleZoneID + "/dayReport?date=" + str(date), headers={"Authorization" : "Bearer" + bearerToken})
    response = json.loads(r.text)
    
    zoneName = zone_names[int(singleZoneID) - 1]
    logname = str(date) + "_" + zoneName
    
    path = (str(date) + "/")
    if not os.path.exists(path):
        os.makedirs(path)
    
    f=open(str(date) + "/" + logname + ".json", "w")
    f.write(json.dumps(response, indent=1))
    f.close
    
    createLog(path, logname)
    


#------------------------------------------

#request the bearerToken with username, password & client_secret. The bearerToken will expire after 600 seconds.
r=requests.post("https://auth.tado.com/oauth/token", data={'client_id' : 'tado-web-app', 'grant_type' : 'password', 'scope' : 'home.user', 'username' : username, 'password' : password, 'client_secret' : client_secret})
json_data=json.loads(r.text)
bearerToken=json_data['access_token']


#finding the homeId
r=requests.get("https://my.tado.com/api/v1/me", headers={"Authorization" : "Bearer" + bearerToken})
json_data=json.loads(r.text)
homeId=str(json_data['homeId'])

#----- Change this to what exactly you want to do
#getHistory()
getHistoryRange()
#getZones()
