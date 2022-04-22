import config
import urllib3
import json
import time
#import thread
from time import sleep
from Class import member


def mess(sock, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(config.CHAN, message).encode("utf-8"))


def give_rasa(rasa, nick):
    stop = False
    if len(config.users) != 0:
        for i in config.users:    
            if i.name == nick:
                stop = True
                break    
                
                with open('Data/Rasa.json', 'w') as file:
                    json.dump(config.rasa, file, ensure_ascii=False)
            
        if not stop :
            config.users.append(member(nick,rasa))
            update_index()
    else:
        config.users.append(member(nick,rasa))
        update_index()

def update_index():
    for i in config.users:
        config.index[i.name] = config.users.index(i)
            

