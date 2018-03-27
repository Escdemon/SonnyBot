import os
import time
import re
import json

from slackclient import SlackClient

PATH = "E:/Documents/Bots/SonnyBot"
TOKEN = open(PATH + "/token.txt", "r").read()
END = '_END_'
START = '_START_'

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


with open(PATH + "/data.json") as json_file:
    json_decoded = json.load(json_file)

#json_decoded["Bonjour"] = "END_SENTENCE"

c = sc.api_call(
  "channels.info",
  channel="C7U9SKZEF"
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
    for event in e:
        if event['type'] == "message":
            m = json_decoded
            t = event['text'].split()
            print("t",t)
            #TODO : remove forbidden word in t
            for i,word in enumerate(t):
                print("i,word",i,word)
                if word in m:
                    if m[word] == 'END_SENTENCE':
                        m[word] = t[i+1] if i+1 < len(t) else END
                    m = m[word]
                else:
                    m[word] = t[i+1] if i+1 < len(t) else END
                print(m)
                
            print(json_decoded)
                
                
            '''
            print("i,word",i,word)
            if word in m and m[word] != 'END_SENTENCE':
                m = m[word]
            else: 
                print("m",m)
                print("m[" + word + "]",t[i+1] if i+1 < len(t) else 'END_SENTENCE')
                m[word] = t[i+1] if i+1 < len(t) else 'END_SENTENCE'
            print(m)
        print(json_decoded)
            #with open(PATH + "/data.json", 'w') as json_file:
             #   json.dump(json_decoded, json_file)'''



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
        
        