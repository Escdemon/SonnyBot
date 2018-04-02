import time
import json
import sys

from random import randint
from slackclient import SlackClient

TOKEN = open("token.txt", "r").read()
END = '_END_'
START = '_START_'
NICK = '_NICK_'
NICK_LIST = ["sonny", "<@U87N79D25>".lower()]
DATA_FILE = "data.json"
CUTTIE_DATA_FILE = "cuttie-data.json"
CUTTIE_ID = "<@U87N79D25>"

sc = SlackClient(TOKEN)

#User list
userList = sc.api_call("users.list")
users = {}
for i in userList['members']:
    profile = i['profile']
    if profile['display_name'] == '':
        users[i['id']] = profile['real_name']
    else:
        users[i['id']] = profile['display_name']

# Channel list
channelList = sc.api_call("channels.list", exclude_archived = 1)
for i in channelList['channels']:
    print(i['name'] + " " + i['id'])
    
groupList = sc.api_call("groups.list", exclude_archived = 1)

# Load Data
with open(DATA_FILE) as json_file:
    jsonData = json.load(json_file)


def sendMessage(msg, channelTarget):
    sc.api_call(
      "chat.postMessage",
      channel = channelTarget,
      text = msg,
      as_user = "true"
    )


def treatEvent(e):
    for event in e:
        if event['type'] == "message" and event['user'] != 'U87N79D25':
            t = event['text'].split()
            for i,e in enumerate(t):
                if e.lower() in NICK_LIST:
                    t[i] = NICK
            #TODO : remove forbidden word in t
            if t[0] not in jsonData[START]:
                jsonData[START][t[0]] = 1
            else:
                jsonData[START][t[0]] += 1
            for i,word in enumerate(t):
                nextword = t[i+1] if i+1 < len(t) else END
                if word not in jsonData:
                    jsonData[word] = {}
                    jsonData[word][nextword] = 0
                if nextword not in jsonData[word] :
                    jsonData[word][nextword] = 1
                else:
                    jsonData[word][nextword] += 1
            print(jsonData)
            with open(DATA_FILE, 'w') as jsonFile:
               json.dump(jsonData, jsonFile)
                
def sentenceToSay():
    r = []
    m = START
    while m != END:
        score = 0
        tmp = ""
        total = sum(jsonData[m].values())
        rand = randint(0, total-1)
        for i in jsonData[m]:
            score += jsonData[m][i]
            if score > rand:
                tmp = i
                break
        if tmp == END:
            break
        r += [tmp]
        m = tmp
    return ' '.join(r)
    

def sendResponse(e):
    # peut être juste prendre le premiers event ?
    for event in e:
        if event['type'] == "message":
            text = event['text'].lower().split()
            if any(word in text for word in NICK_LIST):
                text = ["Bob" if any(x == word for word in NICK_LIST) else x for x in text]
                #print(text)
                sentence = sentenceToSay().replace(NICK, users[event['user']])
                #print(sentence)
                sendMessage(sentence, event['channel'])
                

while True:
    try:
        connect = sc.rtm_connect(auto_reconnect=True)
        #print(connect)
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
    except KeyboardInterrupt:
        sys.exit()
    except:
        continue

