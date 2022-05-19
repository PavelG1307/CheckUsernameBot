from pyrogram import Client, idle
from pyrogram.raw import functions
from threading import Thread
from pyrogram.errors import FloodWait, UsernameInvalid
import time
from datetime import datetime 
from pyrogram.handlers import MessageHandler


n = 7

mybot=Client(
    "my_bot",
    bot_token="5372427759:AAHdw3tUd7apEIkSIpoP2cNkRoUffFZOuCY",
    api_id=19852685,
    api_hash="724fe0f06ef691717c16d28c39430506"
)

api_id=19852685
api_hash = "724fe0f06ef691717c16d28c39430506"

my_apps = []

for i in range(n):
    my_apps.append(Client(f'account{i}', api_id = api_id, api_hash = api_hash))

usernamearr=[]
idusersarr=[]

channelarr=[]
idapp=[]
iduserchannel=[]

users=[]

newiduserchannel=[]
workacc=0
asyncfl=True
fl = False
flo = False
fl2=False
firstreq=True
svusername=""
svid=""
intime=0
timereq=[]
password="gkcpVfPB"
tokken="ajkasjd"

def openfromfile():
    global idusersarr
    global usernamearr
    global users
    f = open('tracked_username.txt', 'r+')
    usernamearr=[]
    idusersarr=[]
    lines = f.readline().split(" ")
    for i in range(0,len(lines)//2):
        usernamearr.append(lines[2*i])
        idusersarr.append(int(lines[2*i+1]))
    f.close()
    f = open('tracked_channel.txt', 'r+')
    lines = f.readline().split(" ")
    for i in range(0,len(lines)//3):
        channelarr.append(lines[3*i])
        iduserchannel.append(int(lines[3*i+1]))
        idapp.append(int(lines[3*i+2]))
    f.close()
    f = open('users', 'r+')
    lines = f.readline().split(" ")
    
    for i in range(0,len(lines)//2):
        users.append(int(lines[2*i]))
    f.close()



def saveinfile(fl):
    if fl:
        f = open('tracked_username.txt', 'w+')
        f.truncate(0)
        savestr=""
        for i in range(0,len(usernamearr)):
            savestr+=str(usernamearr[i]) + " " + str(idusersarr[i])+" " 
        f.write(savestr)
            # f.write(str(idusersarr[i]))
        f.close()
    else:
        f = open('tracked_channel.txt', 'w+')
        f.truncate(0)
        savestr=""
        for i in range(0,len(channelarr)):
            savestr+=str(channelarr[i]) + " " + str(iduserchannel[i])+" "+str(idapp[i])+" " 
        f.write(savestr)
        f.close()

def saveusers(id):
    global users
    users.append(id)
    f = open('users', 'w+')
    f.truncate(0)
    savestr=""
    for i in range(0,len(users)):
        savestr+=str(users[i]) + " 0 "
    f.write(savestr)
    f.close()

def changeaccount():
    global workacc
    global my_apps
    workacc+=1
    if workacc>=len(my_apps): workacc=0
    print("changeaccount")


def listname(idch, passw):
    global usernamearr
    # global idusersarr
    global idchat
    answ=""
    if passw==password:
        for name in usernamearr:
            answ+=name+"\n"
        pass
    else:
        for i in range(len(usernamearr)):
            if(idch==idusersarr[i]): answ+=usernamearr[i]+"\n"
    if(answ==""):
        answ="Нет отслеживаемых username'ов!" 
    else:
        answ="Отслеживаемые username'ы:\n"+answ

    return answ

def listtime():
    global timereq
    if len(timereq)!=0:
        answ="Время мониторинга:\n"
        for i in range(len(timereq)):
           answ+= str(timereq[i]//60).rjust(2,"0")+":"+str(timereq[i]%60).rjust(2,"0")+"\n"
    else:
        answ="Время мониторинга не задано!" 
    return answ

def listchannel(id, passw):
    answ=""
    if passw!=password:
        for i in range(len(channelarr)):
            if (id==iduserchannel[i]):
                answ+=channelarr[i]+"\n"
        if answ=="":
            answ="Доступных username'ов нет!" 
        else: 
            answ="Доступные username'ы:\n"+answ
    else:
        answ="Доступные username'ы:\n"
        for i in range(len(channelarr)):
            answ+=channelarr[i]+"\n"
    return answ

countcreatechannel=0

def createchannel(name, id):
    global channelarr
    global iduserchannel
    global idapp
    global countcreatechannel
    try:
        countcreatechannel+=1
        if(countcreatechannel>2):
            changeaccount()
            countcreatechannel=0
        if len(channelarr)>len(my_apps)*16-1:
            mybot.send_message(id, "Бот переполнен! Невозможно зарезервировать " + name)
        else:
            my_apps[workacc].update_chat_username(my_apps[workacc].create_channel(name).id, name)

    except FloodWait as e:
            changeaccount()
            mybot.send_message(id, "Достигнут лимит! Ограничение на: " + str(e.x)+" секунд! Включен аккаунт: " + str(workacc+1))
            createchannel(name, id)
            return
    except Exception:
        mybot.send_message(id, "Ошибка, меняю аккаунт!")
        changeaccount()
        createchannel(name, id)
        return
    else:
        channelarr.append(name)
        iduserchannel.append(id)
        idapp.append(workacc)
        mybot.send_message(id, "Username: " + name + " забронирован!")
        fl=False
    saveinfile(False)

def deletechanel(name,message):
    global idapp
    global channelarr
    global iduserchannel
    global countcreatechannel
    if name in channelarr:
        if message.chat.id==iduserchannel[channelarr.index(name)]:
            try:
                my_apps[idapp[channelarr.index(name)]].delete_channel(name)
            except FloodWait as e:
                    changeaccount()
                    message.reply("Достигнут лимит! Ожидайте: " + str(e.x)+" секунд! Включен аккаунт: " + str(workacc+1))
                    return False
            except Exception:
                message.reply("Ошибка!")
            else:
                idapp.pop(channelarr.index(name))
                iduserchannel.pop(channelarr.index(name))
                channelarr.remove(name)
                message.reply("Username: " + name + " освобожден!")
        else:
                message.reply("Не доступа!")
        saveinfile(False)

    else:
        message.reply("Username: " + message.text[9:] + " не найден в списке доступных username'ов!")

def sendallusers(text):
    for user in users:
        mybot.send_message(user, text)


def follow():
    global asyncfl
    global svusername
    global usernamearr
    global timereq
    global idusersarr
    global firstreq
    global workacc
    global my_apps
    global newiduserchannel
    now=-1

    
    while(asyncfl):
        time.sleep(59)
        available=False
        print("...")
        # now = int(datetime.now().hour)*60+int(datetime.now().minute)+3*60
        now = int(datetime.now().hour)*60+int(datetime.now().minute)
        for i in range(len(timereq)):
            if timereq[i]==now and firstreq:
                count=0
                count2=0
                newiduserchannel=[]
                print("Check!")
                firstreq=False
                for i in range(len(usernamearr)):
                    try:
                        count+=1
                        if my_apps[workacc].send(functions.account.CheckUsername(username=usernamearr[i])):
                            createchannel(usernamearr[i],idusersarr[i])
                            newiduserchannel.append(idusersarr[i])
                            usernamearr.remove(usernamearr[i])
                            idusersarr.remove(idusersarr[i])
                            saveinfile(True)
                            available=True
                            count2+=1
                            count+=2
                        if count>4:
                            changeaccount()    
                            count=0
                        if (count2>len(my_apps)*2):
                            time.sleep(60-len(my_apps)*2) 
                        time.sleep(1)
                    except UsernameInvalid:
                        if count>4:
                            changeaccount()    
                            count=0
                        if (count2>len(my_apps)*2):
                            time.sleep(60-len(my_apps)*2) 
                        time.sleep(1)
                    except FloodWait as e:
                        fl=False
                        flo=False
                        i-=1
                        changeaccount()
                        print("Достигнут лимит! Ограничение на: " + str(e.x)+" секунд! Включен аккаунт: " + str(workacc+1))
                        sendallusers("Достигнут лимит! Ограничение на: " + str(e.x)+" секунд! Включен аккаунт: " + str(workacc+1))
                    except Exception:
                        sendallusers("Произошла ошибка!")
                        i-=1
                        changeaccount()
                if not available: 
                    for user in users:
                        if not (user in newiduserchannel):
                            mybot.send_message(user, "Произошел опрос юзернеймов, доступных не обнаруженно!")
            else:
                firstreq=True
    
openfromfile()



thread1 = Thread(target=follow, args=())
thread1.start()


print("Bot started!")

@mybot.on_message()
def hello(client, message):
    global fl
    global fl2
    global flo
    global svusername
    global usernamearr
    global asyncfl 
    global intime
    global timereq
    global channelarr
    global idusersarr
    global password
    
    fl2=False

    if message.chat.id in users:
        if intime==message.chat.id:
            timereq=[]
            intime=0
            fl2=True
            answ=message.text.split(' ')
            for i in range(0,len(answ),1):
                timereq.append((int(answ[i].split(':')[0]))*60+(int(answ[i].split(':')[1])))
            message.reply(listtime())

        if message.text.find("/start")!=-1 or message.text=="/help":
            fl2=True
            message.reply("Введите ‘Username’, чтобы забронировать его или начать отслеживать\nДля взаимодействия с ботом используйте следующие команды:\n/trackednames – список отслеживаемых username’ов\n/avaiblenames  – список «забронированных» username’ов\n/release – отменить «бронирование» username’а из списка\n/stop – остановить отслеживание username’а из списка\n/help – список команд")
        if message.text=="/help_"+password:
            fl2=True
            message.reply("Расширенные возможности:\n/time_" + password + " – установить время проверки username’ов\n/listall_"+password+" – список отслеживаемых username’ов\n/allavaiblenames_"+password+"  – список «забронированных» username’ов\n/stopall_"+ password +" – очистить список отслеживаемых username’ов\n/changeaccount – принудительно сменить рабочий аккаунт\n/changepassword_"+password+"_'новый_пароль' – установить новый пароль")
    
        if message.text.find("/changepassword_"+password)!=-1:
            password=message.text[17+len(password):]
            fl2=True
            message.reply("Новый пароль: " + str(password))
    
        if message.text=="/time_"+password:
            intime=message.chat.id
            fl2=True
            message.reply("Введите время опроса в формате: ХХ:ХХ YY:YY ZZ:ZZ")       
        
        if message.text=="/changeaccount":
            changeaccount()
            message.reply("Запущен " + str(workacc+1) + " аккаунт")
            fl2=True

        if message.text.find("/stop_")!=-1:
            fl2=True
            try:
                if idusersarr[usernamearr.index(message.text[6:].lower())]==message.chat.id:
                    idusersarr.pop(usernamearr.index(message.text[6:].lower()))
                    usernamearr.remove(message.text[6:].lower()) 
            except Exception:
                message.reply("Ошибка!")
            else:
                saveinfile(True)
                message.reply("Отслеживание " + message.text[6:] + " остановленно!\n")

        if message.text.find("/listall")!=-1:
            fl2=True
            message.reply("Отслеживается " + str(len(usernamearr)) + " username'ов:\n" + listname(message.chat.id, message.text[9:])) 

        if message.text.find("/stopall_"+ password)!=-1: 
            fl2=True
            usernamearr=[]
            idusersarr=[]
            message.reply(listname(message.chat.id, message.text[9:]))   
            saveinfile(True) 

        if message.text=="/stop":
            fl2=True
            answ=""
            for i in range(0,len(usernamearr),1):
                if message.chat.id==idusersarr[i]:
                    answ+="/stop_" + usernamearr[i]+"\n"
            if answ=="":
                answ="Нет отслеживаемых username'ов\n" 
            message.reply(answ)
            

        if message.text=="/trackednames": 
            fl2=True
            message.reply(listname(message.chat.id,0))
        
        if message.text=="/avaiblenames":
            fl2=True
            message.reply(listchannel(message.chat.id,0))

        if message.text=="/allavaiblenames_" + password:
            fl2=True
            message.reply(listchannel(message.chat.id, password))

        if message.text.find("/release_")!=-1:
            fl2=True
            if (message.chat.id==iduserchannel[channelarr.index(message.text[9:])]):
                deletechanel(message.text[9:].lower(), message)

        if message.text.find("/release")!=-1 and not fl2:
            fl2=True
            answ=""
            for uname in channelarr:
                if (message.chat.id==iduserchannel[channelarr.index(uname)]):
                    answ+="/release_" + uname +"\n"
            if answ=="": answ="Доступных username'ов нет!"
            else: answ="Выберите username:\n" + answ
            message.reply(answ)
        



        if message.text=="/botstop": 
            fl2=True
            print("Bot stoped!") 
            asyncfl=False
            thread1.join()
            quit()
        


        if fl2==False:
            svusername=message.text.lower()
            if svusername in usernamearr:
                message.reply("Данный username уже отслеживается!")
            else:
                try:
                    if my_apps[workacc].send(functions.account.CheckUsername(username=svusername)):
                        createchannel(svusername,message.chat.id)
                    else:
                        usernamearr.append(svusername)
                        idusersarr.append(message.chat.id)
                        message.reply("Отслеживание " + svusername + " запущено!\nОтслеживаемые username'ы: /trackednames")
                        saveinfile(True)
                except FloodWait as e:
                    fl=False
                    flo=False
                    changeaccount()
                    print("Достигнут лимит! Ограничение на: " + str(e.x)+" секунд! Включен аккаунт: " + str(workacc+1))
                    message.reply("Достигнут лимит! Ограничение на: " + str(e.x)+" секунд! Включен аккаунт: " + str(workacc+1))
                except UsernameInvalid:
                    usernamearr.append(svusername)
                    idusersarr.append(message.chat.id)
                    saveinfile(True)
                    message.reply("Некорректный или заблокированный username!\nОтслеживание " + svusername + " запущено!\nОтслеживаемые username'ы: /trackednames")
    else:
        if message.text=="/start_"+tokken:
                saveusers(message.chat.id)
                message.reply("Введите ‘Username’, чтобы забронировать его или начать отслеживать\nДля взаимодействия с ботом используйте следующие команды:\n/trackednames – список отслеживаемых username’ов\n/avaiblenames  – список «забронированных» username’ов\n/release – отменить «бронирование» username’а из списка\n/stop – остановить отслеживание username’а из списка\n/help – список команд")



mybot.start()
for app in my_apps:
    app.start()

idle()

mybot.stop()
for app in my_apps:
    app.stop()
