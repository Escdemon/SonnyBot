import os
import time
import re
import json

from random import randint
from slackclient import SlackClient

PATH1 = "E:/Documents/Bots/SonnyBot"
PATH2 = "C:/Users/paul.neissen/Documents/Bots/SonnyBot"
PATH = PATH2
TOKEN = open(PATH + "/token.txt", "r").read()
END = '_END_'
START = '_START_'
NICK = '_NICK_'


sc = SlackClient(TOKEN)

#Target channel #testsonny #paul.neissen #alice.montel
target = "alice.montel"


#User list
userList = sc.api_call("users.list")
users = {}
for i in userList['members']:
    #print(i['name'] + " " + i['id'])
    if i['name'] == target:
        target = i['id']
    if i['profile']['display_name'] == '':
        users[i['id']] = i['profile']['real_name']
    else:
        users[i['id']] = i['profile']['display_name']

# Channel list
channelList = sc.api_call(
  "channels.list",
  exclude_archived=1
)
'''
for i in channelList['channels']:
    print(i['name'] + " : " + i['id'])'''

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


def sendMessage(msg, channelTarget):
    sc.api_call(
      "chat.postMessage",
      channel=channelTarget,
      text=msg,
      as_user = "true"
    )

def treatEvent(e):
    for event in e:
        if event['type'] == "message" and event['user'] != 'U87N79D25':
            m = START
            t = event['text'].split()
            for i,e in enumerate(t):
                if e.lower() in ["sonny", "<@U87N79D25>".lower()]:
                    t[i] = NICK
            #TODO : remove forbidden word in t
            if t[0] not in json_decoded[START]:
                json_decoded[START][t[0]] = 1
            else:
                json_decoded[START][t[0]] += 1
            for i,word in enumerate(t):
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
                
def sentenceToSay():
    r = []
    m = START
    while m != END:
        print("while: ",m)
        score = 0
        tmp = ""
        total = sum(json_decoded[m].values())
        rand = randint(0, total-1)
        print("total: ", total)
        print("rand: ", rand)
        for i in json_decoded[m]:
            score += json_decoded[m][i]
            print(score, i)
            if score > rand:
                tmp = i
                break
            '''
            print(i)
            if json_decoded[m][i] > maxScore and i.lower() not in ["sonny", "<@U87N79D25>".lower()]:
                maxScore = json_decoded[m][i]
                tmp = i'''
        if tmp == END:
            break
        r += [tmp]
        m = tmp
        print(r)
    return ' '.join(r)
    
def sendResponse(e):
    for event in e:
        if event['type'] == "message":
            text = event['text'].lower().split()
            if any(word in text for word in ["sonny", "<@U87N79D25>".lower()]):
                text = ["Bob" if any(x==word for word in ["sonny", "<@U87N79D25>".lower()]) else x for x in text]
                print(text)
                sentence = sentenceToSay().replace(NICK, users[event['user']])
                print(sentence)
                sendMessage(sentence, event['channel'])


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
                sendResponse(e)
                
                

            time.sleep(1)
        print("End")
    else:
        print("Connection Failed")

