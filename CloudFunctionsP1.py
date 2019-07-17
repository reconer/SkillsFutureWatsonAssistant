#####################################################################
#                                                                   #
# SkillsFuture IBM Cloud Function Example                           #
#   This example is used to show how to get data from data.gov.sg   #
#   and return it to Watson Assistant.                              #
#                                                                   # 
# input JSON: { "officeLocation": "Changi"}                         #
#                                                                   #
# WL IBM - 17 July 2019                                             #
#                                                                   #  
#####################################################################

import sys
import json
import requests

#our function
def GetForecast(area,forecastsData):
    for a_forecast in forecastsData:
        if area in a_forecast["area"].lower():
            return a_forecast["forecast"]

def main(dict):
    
    #create defaults for our variables
    officeLocation = "changi"
    
    #first, lets deconstruct the input variable, convert it to lower caps this will make searching easier
    if "officeLocation" in dict:
        officeLocation = dict["officeLocation"]
        officeLocation = officeLocation.lower()

    #the action below will get data from data.gov.sg, save it as responseData
    response = requests.get('https://api.data.gov.sg/v1/environment/2-hour-weather-forecast')
    responseData = response.json()
    forecastsData = responseData["items"][0]["forecasts"]
    
    #this will extract the forecast for the area, for example, Changi
    forecastArea = GetForecast(officeLocation,forecastsData)
    
    #craft our return data. the return data must be JSON
    results = {
        "area" : officeLocation,
        "forecast" : forecastArea
    }
    
    return results
