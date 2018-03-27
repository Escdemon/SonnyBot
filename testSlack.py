import os
import time
import re
import json
from slackclient import SlackClient

PATH = "C:/Users/paul.neissen/Documents/Bots/SonnyBot"
TOKEN = open(PATH + "/token.txt", "r").read()

sc = SlackClient(TOKEN)

#Target channel #testsonny #paul.neissen #alice.montel
target = "paul.neissen" 

#User list
userList = sc.api_call("users.list")
for i in userList['members']:
    print(i['name'] + " " + i['id'])
    if i['name'] == target:
        target = i['id']
        
# Channel list
channelList = sc.api_call(
  "channels.list",
  exclude_archived=1
)
for i in channelList['channels']:
    print(i['name'] + " : " + i['id'])

groupList = sc.api_call(
  "groups.list",
  exclude_archived=1
)
for i in groupList['groups']:
    print(i['name'] + " : " + i['id'])
    if i['name'] == target:
        target = i['id']


        
def sendMessagetest():
    sc.api_call(
      "chat.postMessage",
      channel=target,
      text="Hi :)",
      as_user = "true"
    )

def treatEvent(e):
    a=  0
    

with open(PATH + "/data.json") as json_file:
    json_decoded = json.load(json_file)

json_decoded["Bonjour"] = "END_SENTENCE"

with open(PATH + "/data.json", 'w') as json_file:
    json.dump(json_decoded, json_file)


#sendMessagetest()


while True:
    connect = sc.rtm_connect(auto_reconnect=True)
    print(connect)
    if connect:
        print("Connection Succeed")
        while True:
            e = sc.rtm_read()
            if len(e):
                print(e)
                treatEvent(e)
                
            time.sleep(1)
        print("End")
    else:
        print("Connection Failed")
