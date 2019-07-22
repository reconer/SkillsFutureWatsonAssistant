#####################################################################
#                                                                   #
# SkillsFuture IBM Cloud Function Example 2                         #
#   This example is used to show how to get data from Discovery     #
#   and return it to Watson Assistant.                              #
#                                                                   # 
# input JSON: { "text": "What is Barn Town?"}                       #
#                                                                   #
# WL IBM - 17 July 2019                                             #
#                                                                   #  
#####################################################################
import os
import sys

try:
    from ibm_cloud import DiscoveryV1
except ImportError:
    from watson_developer_cloud import DiscoveryV1

def MakeReturnMessage(results):
    messageback = "Here are some answers from search:<br>\n"
    counter = 0
    for aresult in results:
        counter = counter + 1
        messageback = messageback + "<b>" + str(counter) + "</b> " + aresult["text"] + "<br>\n"
    return messageback        

def main(dict):
    
    #create defaults for our variable
    text = ""
    
    #first, lets deconstruct the input variable
    if "text" in dict:
        text = dict["text"]

    #then create the discovery object, please choose the right version. 
    discovery = ""
    if 'username' in dict:
        discovery = DiscoveryV1(version=dict['version'],  url=dict['url'],
                               username=dict['username'], password=dict['password'])    
    elif 'iam_apikey' in os.environ:
        discovery = DiscoveryV1(version=dict['version'], url=dict['url'],
                                iam_apikey=dict['iam_apikey'] )
    else:
        return { 'text': 'Error: Disc. Creds not specified!' }
    
    #query discovery
    get_disc = discovery.query(dict['envid'], dict['colid'], natural_language_query=text, count=3)
    
    #get results
    get_results = get_disc.get_result()['results']
    
    #make the output message
    messageback = ""
    if len(get_results) > 0:
        messageback = MakeReturnMessage(get_results)
    else:
        messageback = "I am sorry, there are no results from search. Please try another question"
    
    #craft the output
    result = {"text":messageback}
    
    return result