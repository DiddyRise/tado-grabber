#!/bin/python3

from datetime import date
import json
import os
from dateutil import parser

#------Temp & Hum Log + Valve State--------------
def findCallForHeatForMeasure(cfhList, measureDate):
    cfhs = [i["value"] for i in cfhList if parser.parse(str(i["from"]), ignoretz=True) <= measureDate <= parser.parse(str(i["to"]), ignoretz=True)]

    return "ERROR" if len(cfhs) == 0 else cfhs[0]

def findOutsideTempForMeasure(otList, measureDate):
    ots = [i["value"]["temperature"]["celsius"] for i in otList if parser.parse(str(i["from"]), ignoretz=True) <= measureDate <= parser.parse(str(i["to"]), ignoretz=True)]

    return "ERROR" if len(ots) == 0 else ots[0]

def findHeatEnabledForMeasure(heList, measureDate):
    hes = [i["value"]["power"] for i in heList if parser.parse(str(i["from"]), ignoretz=True) <= measureDate <= parser.parse(str(i["to"]), ignoretz=True)]

    return "ERROR" if len(hes) == 0 else hes[0]


def createLog(path, logname):
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir,path + logname + ".json")
    csvname = os.path.join(dir,path + logname + ".csv")

    f = open(csvname, "w")
    f.write("Date (UTC),Temperature,Humidity,Valve State,Outside Temperature,Heating State" + "\n")

    with open(filename) as jsonFile:
        data = json.load(jsonFile)

        dataTemp = data["measuredData"]["insideTemperature"]["dataPoints"]
        dataHumid = data["measuredData"]["humidity"]["dataPoints"]
        dataValves = data["callForHeat"]["dataIntervals"]
        dataOutside = data["weather"]["condition"]["dataIntervals"]
        dataHeatOn = data["settings"]["dataIntervals"]



        for i, dataPointsTemperature in enumerate(dataTemp):

            csvLine = []

            date = parser.parse(str(dataPointsTemperature["timestamp"]), ignoretz=True)
            csvLine.append(str(date))
            csvLine.append(str(dataPointsTemperature["value"]["celsius"]))
            csvLine.append(str(dataHumid[i]["value"]))
            csvLine.append(str(findCallForHeatForMeasure(dataValves, date)))
            csvLine.append(str(findOutsideTempForMeasure(dataOutside, date)))
            csvLine.append(str(findHeatEnabledForMeasure(dataHeatOn, date)))

            f.write(','.join(csvLine) + '\n')

        f.close()

#----------------------------------
#--------Min/Max------------------

    with open(filename) as jsonFile:
        data = json.load(jsonFile)

    min = data["measuredData"]["insideTemperature"]["min"]["celsius"]
    max = data["measuredData"]["insideTemperature"]["max"]["celsius"]
        
        
    f = open(csvname, "a")
    f.write("\n" + "Indoor Minimum Temperature,Indoor Maximum Temperature" + "\n")
    f.write(str(min) + "," + str(max) + "\n")
    f.close

#----------------------------------
#-------Valve Log------------------

    valveStatus = []

    with open(filename) as jsonFile:
        data = json.load(jsonFile)

    for dataPointsValve in data["callForHeat"]["dataIntervals"]:
        date_start = parser.parse(str(dataPointsValve["from"]), ignoretz=True)
        date_end = parser.parse(str(dataPointsValve["to"]), ignoretz=True)
        valveStatus.append(str(date_start) + "," + str(date_end) + "," + str(dataPointsValve["value"]))
        
    i = 0
    f = open(csvname, "a")
    f.write("\n" + "From (UTC),To (UTC),Valve State" + "\n")
    for each in valveStatus:
        f.write(valveStatus[i] + "\n")
        i = i + 1
    f.close

#-----------------------------------
#---------Weather Log---------------

    weatherStatus = []

    with open(filename) as jsonFile:
        data = json.load(jsonFile)

    for dataPointsWeather in data["weather"]["condition"]["dataIntervals"]:
        date_start = parser.parse(str(dataPointsWeather["from"]), ignoretz=True)
        date_end = parser.parse(str(dataPointsWeather["to"]), ignoretz=True)
        weatherStatus.append(str(date_start) + "," + str(date_end) + "," + str(dataPointsWeather["value"]["state"]) + "," + str(dataPointsWeather["value"]["temperature"]["celsius"]))
        
    i = 0
    f = open(csvname, "a")
    f.write("\n" + "From (UTC),To (UTC),Weather,Outside Temperature in Celsius" + "\n")
    for each in weatherStatus:
        f.write(weatherStatus[i] + "\n")
        i = i + 1
    f.close

#---------------------------------
