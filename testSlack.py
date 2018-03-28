import os
import time
import re
import json

from slackclient import SlackClient

PATH1 = "E:/Documents/Bots/SonnyBot"
PATH2 = "C:/Users/paul.neissen/Documents/Bots/SonnyBot"
PATH = PATH1
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
            m = START
            t = event['text'].split()
            #t = ['Bonjour']
            print("t",t)
            #TODO : remove forbidden word in t
            if t[0] not in json_decoded[START]:
                json_decoded[START][t[0]] = 1
            else:
                json_decoded[START][t[0]] += 1
            for i,word in enumerate(t):
                
                #TODO si c'est le dernier mot
                #if i == len(t) - 1:
                #   json_decode[word] += [END]
                nextword = t[i+1] if i+1 < len(t) else END
                if word not in json_decoded:
                    json_decoded[word] = {}
                    json_decoded[word][nextword] = 0
                if nextword not in json_decoded[word] :
                    json_decoded[word][nextword] = 1
                else:
                    json_decoded[word][nextword] += 1
            print(json_decoded)
            with open(PATH + "/data.json", 'w') as json_file:
               json.dump(json_decoded, json_file)
                
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

#treatEvent({})


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

