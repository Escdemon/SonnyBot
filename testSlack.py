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
CUTTIE_ID = "<@U7UG5HLLV>"
CUTTIE = "U7UG5HLLV"
MUSIC_CHAN = 'G9YB0SM96'

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
    
# Load Data
with open(CUTTIE_DATA_FILE) as json_file:
    jsonCuttieData = json.load(json_file)

def sendMessage(msg, channelTarget):
    sc.api_call(
      "chat.postMessage",
      channel = channelTarget,
      text = msg,
      as_user = "true"
    )

def saveCuttieData(t):
    for i,e in enumerate(t):
        if e.lower() in NICK_LIST:
            t[i] = NICK
    #TODO : remove forbidden word in t
    if t[0] not in jsonCuttieData[START]:
        jsonCuttieData[START][t[0]] = 1
    else:
        jsonCuttieData[START][t[0]] += 1
    for i,word in enumerate(t):
        nextword = t[i+1] if i+1 < len(t) else END
        if word not in jsonCuttieData:
            jsonCuttieData[word] = {}
            jsonCuttieData[word][nextword] = 0
        if nextword not in jsonCuttieData[word] :
            jsonCuttieData[word][nextword] = 1
        else:
            jsonCuttieData[word][nextword] += 1
    #print(jsonCuttieData)
    with open(CUTTIE_DATA_FILE, 'w') as jsonFile:
       json.dump(jsonCuttieData, jsonFile)

def treatEvent(e):
    for event in e:
        if 'text' in event:
            if event['type'] == "message" and event['user'] != 'U87N79D25'  and event['channel'] != MUSIC_CHAN:
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
                #print(jsonData)
                with open(DATA_FILE, 'w') as jsonFile:
                   json.dump(jsonData, jsonFile)
                   
                if any(x == CUTTIE_ID for x in t):
                    saveCuttieData(t)
                
def sentenceToSay(data):
    r = []
    m = START
    while m != END:
        score = 0
        tmp = ""
        total = sum(data[m].values())
        rand = randint(0, total-1)
        for i in data[m]:
            score += data[m][i]
            if score > rand:
                tmp = i
                break
        if tmp == END:
            break
        r += [tmp]
        m = tmp
    return ' '.join(r)
    

def sendResponse(e):
    # peut être juste prendre le premier event ?
    for event in e:
        if event['type'] == "message":
            if 'text' in event:
                t = event['text'].split()
                text = event['text'].lower().split()
                if any(word in text for word in NICK_LIST):
                    text = ["Bob" if any(x == word for word in NICK_LIST) else x for x in text]
                    #print(text)
                    
                    sentence = sentenceToSay(jsonCuttieData if event['user'] == CUTTIE else jsonData).replace(NICK, users[event['user']])
                    #print(sentence)
                    sendMessage(sentence, event['channel'])
                

def music(e):
    for event in e:
        if 'text' in event:
            if event['type'] == "message" and event['channel'] == MUSIC_CHAN:
                
                t = event['text'].split()
                text = event['text'].lower().split()
                if any(word in text for word in NICK_LIST) and any(word == 'music' for word in text):
                    #open file
                    d = {}
                    with open('music.txt') as f:
                        content = f.readlines()
                        for line in content:
                            tmp = line.split()
                            if tmp[0] not in d:
                                d[tmp[0]] = [tmp[1]]
                            else:
                                d[tmp[0]] += [tmp[1]]
                    #print(d)
                    
                    if any(word == 'add' for word in text):
                        t = [x for x in t if x not in ['music','Music','MUSIC','metal','Metal','METAL','Dub','dub','DUB',
                                                       'reggae','Reggae','REGGAE','<@U87N79D25>','Sonny','sonny','SONNY',
                                                       'add','Add','ADD','other','Other']]
                        with open('music.txt', 'a') as file:
                            written = True
                            if any(word == 'metal' for word in text):
                                file.write('METAL ' + ''.join(t) + '\n')
                            elif any(word == 'dub' for word in text):
                                file.write('DUB ' + ''.join(t) + '\n')
                                sendMessage(' '.join(d['METAL']), event['channel'])
                            elif any(word == 'reggae' for word in text):
                                file.write('REGGAE ' + ''.join(t) + '\n')
                            elif any(word == 'other' for word in text):
                                file.write('OTHER ' + ''.join(t) + '\n')
                            else:
                                written = False
                            if written:
                                sendMessage(''.join(t) + " added", event['channel'])
                        return True
                    
                    if any(word == 'metal' for word in text) and 'METAL' in d:
                        sendMessage(' '.join(d['METAL']), event['channel'])
                        return True
                    if any(word == 'other' for word in text) and 'OTHER' in d:
                        sendMessage(' '.join(d['OTHER']), event['channel'])
                        return True
                    if any(word == 'dub' for word in text) and 'DUB' in d:
                        sendMessage(' '.join(d['DUB']), event['channel'])
                        return True
                    if any(word == 'reggae' for word in text) and 'REAGGAE' in d:
                        sendMessage(' '.join(d['REGGAE']), event['channel'])
                        return True
                
    return False

while True:
    #try:
        connect = sc.rtm_connect(auto_reconnect=True)
        #print(connect)
        if connect:
            print("Connection Succeed")
            while True:
                e = sc.rtm_read()
                if len(e):
                    print(e)
                    if not(music(e)):
                        treatEvent(e)
                        sendResponse(e)
                time.sleep(1)
            print("End")
        else:
            print("Connection Failed")
            '''
    except KeyboardInterrupt:
        sys.exit()
    except:
        sys.exit()
        continue'''

