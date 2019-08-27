#####################################################################
#                                                                   #
# SkillsFuture IBM Cloud Function Example                           #
#   This example is used to show how to get data from Wikipedia     #
#   and return it to Watson Assistant.                              #
#                                                                   # 
# input JSON: { "query": "Legend of Zelda"}                         #
#                                                                   #
# WL IBM - 27 Aug 2019                                              #
#                                                                   #  
#####################################################################

import sys
import json
import requests

#our function to build the results for top 3
def WikiQueryResultsBuilder(querydata):
    maxtotalsearchresults = 3
    counter = 1
    results = "Wikipedia Search Results:<br>"
    
    for a_query in querydata:
        if counter <= maxtotalsearchresults:
            title = a_query["title"]
            pageid = a_query["pageid"]
            results = results + '<a href="https://en.wikipedia.org/?curid=' + str(pageid) + '">' + str(counter) + ": " + title + '</a><br>'
        counter = counter + 1
    
    #invalidate our results if no results
    if len(querydata) == 0:
        results = ""
            
    return results


def main(dict):
    
    #create defaults for our variables
    query = ""
    
    #first, lets deconstruct the input variable 
    if "query" in dict:
        query = dict["query"]
        
    #the action below will get data from data.gov.sg, save it as responseData
    response = requests.get('https://en.wikipedia.org/w/api.php?action=query&list=search&utf8=&format=json&srsearch=' + query)
    responsedata = response.json()
    querydata = responsedata["query"]["search"]
    
    #this will extract the forecast for the area, for example, Changi
    resultsquery = WikiQueryResultsBuilder(querydata)
    
    #craft our return data. the return data must be JSON
    results = {
        "results" : resultsquery,
    }
    
    return results