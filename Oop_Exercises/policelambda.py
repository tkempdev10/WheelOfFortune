import csv
from functools import reduce
import json

#Global Variables
policeData = []
policeDataLoc = "911_Calls_DPD.csv"
#Part 1: Importing the data into dictionaries. Row 0 is the headers
def gettingData():
    global policeData
    global policeDataLoc

    # Open up csv file
    with open(policeDataLoc, 'r') as f:
        fcsv = csv.reader(f)

        # Save data as dictionary entries
        lineNumber = 0
        headers = []
        for line in fcsv:
            formattedLine = dict()
            for i in range(len(line)):
                #Getting the headers
                if (lineNumber == 0):
                    headers.append(line[i])
                else:
                    formattedLine[headers[i]] = line[i]
            if (lineNumber != 0):
                policeData.append(formattedLine)
            lineNumber = lineNumber + 1

#Filtering out rows with empty values for neighborhood and zip code responses
def filtering():
    #Global variables
    global policeData

    #Filtering
    policeData = list(filter(lambda row: row['zip_code'] != '', policeData))
    policeData = list(filter(lambda row: row['zip_code'] != 0, policeData))
    policeData = list(filter(lambda row: row['zip_code'] != None, policeData))

    policeData = list(filter(lambda row: row['neighborhood'] != '', policeData))
    policeData = list(filter(lambda row: row['neighborhood'] != 0, policeData))
    policeData = list(filter(lambda row: row['neighborhood'] != None, policeData))

#calculate the average total response time, the average dispatch time, and average total time
#Wth lambda and reduce functions
def lambdaFunctions():
    #Global variables
    global policeData

    #total response time average
    totalTotalResponseTime = reduce(lambda call1, call2: float(call1) + float(call2), policeData["totalresponsetime"])
    print(totalTotalResponseTime/len(policeData['totalresponsetime']))
    #Dispatch time average
    AverageDispatchTime = reduce(lambda call1, call2: float(call1) + float(call2), policeData["dispatchtime"])
    print(AverageDispatchTime/len(policeData['dispatchtime']))
    #Total time average
    AverageTotalTime = reduce(lambda call1, call2: float(call1) + float(call2), policeData["totaltime"])
    print(AverageTotalTime/len(policeData['totaltime']))
