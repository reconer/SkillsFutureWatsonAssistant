#####################################################################
#                                                                   #
# SkillsFuture IBM Cloud Function Example                           #
#   This example is used to show how to get data from WeatherAPI    #
#   and return it to Watson Assistant.                              #
#                                                                   # 
# input JSON: { "lat": 1.3365549, "long":103.9652136}               #
#                                                                   #
# WL IBM - 29 Aug 2019                                              #
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
    #define our empty output
    results = {}
    
    #create defaults for our variables
    lat  = 1.3365549
    long = 103.9652136
    
    #first, lets deconstruct the input variable, convert it to lower caps this will make searching easier
    if "lat" in dict and "long" in dict :
        if isinstance(dict["lat"], float) and isinstance(dict["long"], float):
            lat = dict["lat"]
            long = dict["long"]

    #the action below will get data from data.gov.sg, save it as responseData
    WeatherAPI_url = "https://twcservice.mybluemix.net/api/weather/v1/geocode/" + str(lat) + "/"  + str(long) + "/observations.json?language=en-US"
    WeatherAPI_username = "7d56aa43-cbfb-477b-af69-ddef282c3e6c"
    WeatherAPI_password = "D483qR3lpr"
    response = requests.get(WeatherAPI_url, auth=(WeatherAPI_username, WeatherAPI_password))

    
    #------------------------------------------------------------------------#
    # Example output from response.json() :                                  # 
    #                                                                        #     
    #   {                                                                    #
    #        'metadata': {'latitude': 1.33,'longitude': 103.96,              #
    #    },                                                                  #  
    #    'observation': {                                                    #
    #        'key': 'WSSS',                                                  #
    #        'class': 'observation',                                         #
    #        'expire_time_gmt': 1567056600,                                  #
    #        'obs_id': 'WSSS',                                               # 
    #        'obs_name': 'Changi Arpt',                                      #
    #        'valid_time_gmt': 1567049400,                                   # 
    #        'day_ind': 'D',                                                 # 
    #        'temp': 88,                                                     #  
    #        'wx_phrase': 'Mostly Cloudy', {........}                        # 
    #      }                                                                 #  
    #    }                                                                   #
    #------------------------------------------------------------------------# 
    
    try:
        obs_data = response.json()
        obs_data = obs_data["observation"]
        #craft our return data. the return data must be JSON
        results = {
            "lat" : lat,
            "long" : long,
            "obs_name" : obs_data["obs_name"],
            "forecast" : obs_data["wx_phrase"]
        }
        return results
    except:
        
        response = requests.get('https://api.data.gov.sg/v1/environment/2-hour-weather-forecast')
        responseData = response.json()
        forecastsData = responseData["items"][0]["forecasts"]
        forecastArea = GetForecast("changi",forecastsData)        
        
        print("error",response)
        results = {
            "lat" : lat,
            "long" : long,
            "obs_name" : "changi",
            "forecast" : forecastArea
        }        
        return results
