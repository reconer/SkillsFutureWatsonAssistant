#####################################################################
#                                                                   #
# SkillsFuture IBM Watson Assistant Python Example                  #
#   This example is used to show how we can call Watson Assistant   #
#   from Python code and return to the user.                        #
#                                                                   # 
#                                                                   #
# WL IBM - 17 July 2019                                             #
#                                                                   #  
#####################################################################

import json
from ibm_watson import AssistantV2

#------ define some convenience functions ------#
def GetOutputText(return_response):
    result = ""
    output = return_response['output']['generic']
    for a_generic_output in output:
        result = result + a_generic_output['text'] + "\n"
    return result


#------ API key details below, you can get them from the Watson Assistant Service under Credentials -------#
version = '2019-02-28'
iam_apikey = ''
url = 'https://gateway.watsonplatform.net/assistant/api'

#------- Get your assistant id from the Assistant page in Watson Assistant ------#
assistant_id='abfc419a-e015-41e5-aa45-1222619620c8'

#------- Create an assistant object ------#
assistant = AssistantV2(
    version=version,
    iam_apikey=iam_apikey,
    url=url
)

#------- First thing, get your session id ------#
response = assistant.create_session(assistant_id=assistant_id).get_result()
session_id = response['session_id']
print("Got session_id", session_id)

#------- Send an empty string to the session, to get your welcome message ------#
FirstResponse = assistant.message(
    assistant_id=assistant_id,
    session_id=session_id,
    input={}
).get_result()

FirstResponseOutputText = GetOutputText(FirstResponse)

#This will print out the welcome message
print(FirstResponseOutputText)

#Finally, we will send all user inputs to Watson Assistant
while True:
    ReplyToWatsonData = input ("Your reply >").strip()
    
    SubsequentResponse = assistant.message(
        assistant_id=assistant_id,
        session_id=session_id,
        input={
            'message_type': 'text',
            'text': ReplyToWatsonData
        }
    ).get_result()
    
    SubsequentResponseOutputText = GetOutputText(SubsequentResponse)
    
    print(SubsequentResponseOutputText)


