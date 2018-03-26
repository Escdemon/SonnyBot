import os
import time
import re
import json
from slackclient import SlackClient

TOKEN = open("E:/Documents/Bots/SonnyBot/token.txt", "r").read()

sc = SlackClient(TOKEN)

userList = sc.api_call("users.list")

target = "paul.neissen"

for i in userList['members']:
    #print(i['name'] + " " + i['id'])
    if i['name'] == target:
        target = i['id']
        
def sendMessagetest():
    sc.api_call(
      "chat.postMessage",
      channel=target,
      text="Hello from Python! :tada:",
      #username = "Sonny",
      #icon_url = "https://d3evv04q39b0w5.cloudfront.net/prod/app/pages/home/images/chatbot-person.png",
      as_user = "true"
    )

with open("E:/Documents/Bots/SonnyBot/data.json") as json_file:
    json_decoded = json.load(json_file)

json_decoded["Bonjour"] = "END_SENTENCE"

with open("E:/Documents/Bots/SonnyBot/data.json", 'w') as json_file:
    json.dump(json_decoded, json_file)


print(data)
#sendMessagetest()

'''
if sc.rtm_connect():
    print("Connection Succeed")
    while True:
        e = sc.rtm_read()
        if len(e):
            print(e)
        time.sleep(1)
    print("End")
else:
    print("Connection Failed")
'''