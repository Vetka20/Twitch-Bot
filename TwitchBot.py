import json
import random
import config
import utils
import socket
import time
import re
from time import sleep
#import thread


with open('Data/Rasa.json') as file:
    config.rasa = json.load(file)

s = socket.socket()
s.connect((config.HOST, config.PORT))
s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
s.send("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))

chat_massage = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
utils.mess(s, "Я вернулся Госпожа @{}".format(config.gospoja))
angrymod = False
while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("POND :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0)
        massage = chat_massage.sub("",response)
        print(response)
        ### проверка на наличия команды !*** или на упоминания Тани
        if len(re.findall(r"!\w+", massage)) != 0 or len(re.findall(r"@tanywa_k", massage)) != 0:
            
            #Функция время
            if massage.strip() == "!time":
                utils.mess(s, "Сам узнаешь, @{}. Да и вообще для этого существует другой пушистый".format(username))
                time.sleep(2)
                utils.mess(s, "!Uptime")
            
            #Упоминания слова Госпожа Class
            elif len(re.findall(r"@tanywa_k", massage)) != 0 and len(re.findall(r"\bГоспожа", massage)) == 0 and angrymod:
                if username in config.rasa.keys():
                    utils.mess(s, "@{} {}, забыл с кем разговариваешь? Или ты забыл кто здесь Госопожа?".format(username,random.choice(config.obrash[list(user.relationship for user in config.users if user.name == username)[0]])))
                else:
                    utils.mess(s, "@{}, забыл с кем разговариваешь? Или ты забыл кто здесь Госопожа?".format(username))

            #angrymod
            elif username==config.gospoja and massage.strip() == "!angry-mod":
                angrymod = not angrymod 

            #защита тани от наезда
            elif len(re.findall(r"!деф", massage)) != 0:
                utils.mess(s, "Кто посмел обидеть госпожу!!??")
                            
            #прощание

            #Функция about Class
            elif massage.strip() == "!about":
                if username == config.gospoja:
                    utils.mess(s, "Я Ваш послушний пушистий рабик Госпожа @{}. Сделан Веткой чтобы служить Вам и защищать Вас.".format(config.gospoja))
                elif username in list(user.name for user in config.users) and username != config.gospoja:
                    utils.mess(s, "{} @{}, не собираюсь говорить тебе кто я.".format(random.choice(config.obrash[list(user.relationship for user in config.users if user.name == username)[0]][list(user.rasa for user in config.users if user.name == username)[0]]),username))
                else:
                    utils.mess(s, "@{}, не собираюсь говорить тебе кто я. У тебя даже расы нет. Если хочешь получить расу напиши !get_rasa".format(username))
            
            #Выбор расы
            elif  len(re.findall(r"!im_\w{3,4}", massage)) != 0:
                if massage.strip() == "!im_arg":
                    utils.give_rasa("Аргонианин", username)
                    utils.mess(s, "Так ты у нас {} @{}".format(random.choice(list(config.obrash[config.users[config.index[username]].relationship][config.users[config.index[username]].rasa])), username))
                
                elif massage.strip() == "!im_dan":
                    utils.give_rasa("Данмер", username)
                    utils.mess(s, "Так ты у нас {} @{}".format(random.choice(list(config.obrash[config.users[config.index[username]].relationship][config.users[config.index[username]].rasa])), username))

                elif massage.strip() == "!im_alt":
                    utils.give_rasa("Альтмер", username) 
                    utils.mess(s, "Так ты у нас {} @{}".format(random.choice(list(config.obrash[config.users[config.index[username]].relationship][config.users[config.index[username]].rasa])), username))

                elif massage.strip() == "!im_khaj":
                    utils.give_rasa("Каджит", username) 
                    utils.mess(s, "Так ты у нас {} @{}".format(random.choice(list(config.obrash[config.users[config.index[username]].relationship][config.users[config.index[username]].rasa])), username))

                elif massage.strip() == "!im_bosm":
                    utils.give_rasa("Босмер", username) 
                    utils.mess(s, "Так ты у нас {} @{}".format(random.choice(list(config.obrash[config.users[config.index[username]].relationship][config.users[config.index[username]].rasa])), username))

                elif massage.strip() == "!im_bret":
                    utils.give_rasa("Бретонец", username) 
                    utils.mess(s, "Так ты у нас {} @{}".format(random.choice(list(config.obrash[config.users[config.index[username]].relationship][config.users[config.index[username]].rasa])), username))

                elif massage.strip() == "!im_nord":
                    utils.give_rasa("Норд", username) 
                    utils.mess(s, "Так ты у нас {} @{}".format(random.choice(list(config.obrash[config.users[config.index[username]].relationship][config.users[config.index[username]].rasa])), username))

                elif massage.strip() == "!im_redg":
                    utils.give_rasa("Редгард", username) 
                    utils.mess(s, "Так ты у нас {} @{}".format(random.choice(list(config.obrash[config.users[config.index[username]].relationship][config.users[config.index[username]].rasa])), username))

                elif massage.strip() == "!im_ork":
                    utils.give_rasa("Орк", username) 
                    utils.mess(s, "Так ты у нас {} @{}".format(random.choice(list(config.obrash[config.users[config.index[username]].relationship][config.users[config.index[username]].rasa])), username))

                elif massage.strip() == "!im_imp":
                    utils.give_rasa("Имперец", username) 
                    utils.mess(s, "Так ты у нас {} @{}".format(random.choice(list(config.obrash[config.users[config.index[username]].relationship][config.users[config.index[username]].rasa])), username))

            #Получить случайную расу Class
            elif massage.strip() == "!get_rasa":
                utils.give_rasa("{}".format(random.choice(list(config.obrash[0].keys()))), username)
                utils.mess(s, "Так ты у нас {} @{}".format(random.choice(list(config.obrash[config.users[config.index[username]].relationship][config.users[config.index[username]].rasa])), username))


            #Вывод текущей расы Class
            elif massage.strip() == "!iam":

                if username in list(user.name for user in config.users):
                    user = list(user for user in config.users if user.name==username)
                    utils.mess(s, "Твоя раса - {}".format(user[0].rasa))
                else:
                    utils.mess(s, "Ты похоже еще не определился. Можешь использовать команду !get_rasa для выбора случайной расы")

            #Викторина
            elif massage.strip() == "!викторина" and username == "vetka20" and config.vict==False:
                utils.mess(s, f"Госпожа @{config.gospoja} начала викторину!")
                vopros = random.choice(list(config.victorina.keys()))
                m = "{}  1: {}  2: {}  3: {}  4: {}  Напишите ответ командой !ответ (номер ответа)".format(vopros, config.victorina[vopros][1][0], config.victorina[vopros][2][0], config.victorina[vopros][3][0], config.victorina[vopros][4][0])
                time.sleep(1.5)
                utils.mess(s, m)

                for k,v in config.victorina[vopros].items():
                    if v[1] == 1: 
                        config.otvet = [k, v[0]]

                config.vict = True

            elif massage.strip() == "!результат" and username == "vetka20" and config.vict==True:
                
                utils.mess(s, "Правильный ответ - {}".format(config.otvet[1]))
                for k,v in config.players.items():
                    if v == config.otvet[0]:
                        if k not in config.points:
                            config.points[username] = 1
                        else:
                            config.points[username] = config.points[username] + 1
                        config.winers.append(f"@{username}")
                time.sleep(2)
                utils.mess(s, "Правильно ответили: {}".format(config.winners))

                config.vict = False
                #config.victorina.pop(vopros)
                time.sleep(1.5)
            
            #Запись ответа Class
            elif len(re.findall(r"!ответ \d", massage)) and config.vict==True:
                o = int(re.findall(r"!ответ (\d)", massage)[0])
                list(user for user in config.users if user.name==username)[0].otvet = o
                       
            elif massage.strip() == "!очки":
                if username in list(user.name for user in config.users):
                    utils.mess(s, "@{} {}, у тебя {} очков".format(username, random.choice(config.obrash[config.rasa[username]]), config.players[username]))
                else:
                    utils.mess(s, "@{} у тебя нет очков".format(username))

time.sleep(1)


