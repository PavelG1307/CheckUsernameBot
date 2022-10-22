bot_token = "5206831411:AAH3_lnU98drAyS97s-MUfDjr5gYQnyT56E"
api_id = 17929149
api_hash = "bf4d900c115a3f2ac85385f5a0bfd330"

from pyrogram import Client, idle
from pyrogram.raw import functions
from threading import Thread
from pyrogram.errors import FloodWait, UsernameInvalid
import time
from datetime import datetime
from pyrogram.handlers import MessageHandler
from pyrogram.errors import RPCError, SessionPasswordNeeded, UserDeactivated, UserDeactivatedBan, AuthKeyDuplicated, UsernameNotOccupied, UserNotParticipant, ChatWriteForbidden, SlowmodeWait, ChannelPrivate, ChannelInvalid, ChatAdminRequired

mybot = Client(
    "my_bot",
    bot_token = bot_token,
    api_id = api_id,
    api_hash = api_hash
)

my_apps = []
apps_data = []
usernamearr = []
idusersarr = []

channelarr = []
idapp = []
iduserchannel = []

users = []

newiduserchannel = []
workacc = 0
asyncfl = True
fl = False
flo = False
fl2 = False
firstreq = True
svusername = ""
svid = ""
intime = 0
timereq = []
password = "gkcpVfPB"
tokken = "ajkasjd"
id_user_registration = 0
mode = 0


def openfromfile():
    global idusersarr
    global usernamearr
    global users, accounts_list
    usernamearr = []
    idusersarr = []
    try:
        f = open('tracked_username.txt', 'r')
        lines = f.readline().split(" ")
        for i in range(0, len(lines)//2):
            usernamearr.append(lines[2*i])
            idusersarr.append(int(lines[2*i+1]))
        f.close()
    except:
        f = open('tracked_username.txt', 'w')
        f.close()
    try:
        f = open('tracked_channel.txt', 'r')
        lines = f.readline().split(" ")
        for i in range(0, len(lines)//3):
            channelarr.append(lines[3*i])
            iduserchannel.append(int(lines[3*i+1]))
            idapp.append(int(lines[3*i+2]))
        f.close()
    except:
        f = open('tracked_channel.txt', 'w')
        f.close()
    try:
        f = open('users', 'r')
        lines = f.readline().split(" ")
        for i in range(0, len(lines)//2):
            users.append(int(lines[2*i]))
        f.close()
    except:
        f = open('users', 'w')
        f.close()
    try:
        f = open('./accounts.ini', 'r', encoding='utf-8')
        data = f.readlines()
        for i in range(len(data)):
            my_apps.append(Client('account{i}',session_string = data[i].rstrip(), api_hash = api_hash, api_id = api_id))
        print('В работе ' + str(len(my_apps)) + ' аккаунтов')
    except:
        f = open('./accounts.ini', 'w')
        f.close()



def saveinfile(fl):
    if fl:
        f = open('tracked_username.txt', 'w')
        f.truncate(0)
        savestr = ""
        for i in range(0, len(usernamearr)):
            savestr += str(usernamearr[i]) + " " + str(idusersarr[i])+" "
        f.write(savestr)
        # f.write(str(idusersarr[i]))
        f.close()
    else:
        f = open('tracked_channel.txt', 'w')
        f.truncate(0)
        savestr = ""
        for i in range(0, len(channelarr)):
            savestr += str(channelarr[i]) + " " + \
                str(iduserchannel[i])+" "+str(idapp[i])+" "
        f.write(savestr)
        f.close()


def saveusers(id):
    global users
    users.append(id)
    f = open('users', 'w')
    f.truncate(0)
    savestr = ""
    for i in range(0, len(users)):
        savestr += str(users[i]) + " 0 "
    f.write(savestr)
    f.close()


def save_accounts():
    with open('./accounts.ini', 'w', encoding='utf-8') as fp:
        fp.truncate(0)
        for acc in my_apps:
            print('saving...')
            fp.write(acc.export_session_string() + '\n')
        fp.close


def changeaccount():
    global workacc
    global my_apps
    workacc += 1
    if workacc >= len(my_apps):
        workacc = 0
    print("changeaccount")


def listname(idch, passw):
    global usernamearr
    # global idusersarr
    global idchat
    answ = ""
    if passw == password:
        for name in usernamearr:
            answ += name+"\n"
        pass
    else:
        for i in range(len(usernamearr)):
            if (idch == idusersarr[i]):
                answ += usernamearr[i]+"\n"
    if (answ == ""):
        answ = "Нет отслеживаемых username'ов!"
    else:
        answ = "Отслеживаемые username'ы:\n"+answ

    return answ


def listtime():
    global timereq
    if len(timereq) != 0:
        answ = "Время мониторинга:\n"
        for i in range(len(timereq)):
            answ += str(timereq[i]//60).rjust(2, "0")+":" + \
                str(timereq[i] % 60).rjust(2, "0")+"\n"
    else:
        answ = "Время мониторинга не задано!"
    return answ


def listchannel(id, passw):
    answ = ""
    if passw != password:
        for i in range(len(channelarr)):
            if (id == iduserchannel[i]):
                answ += channelarr[i]+ " - аккаунт: " + apps_data[idapp[i]]['phone'] + "\n"
        if answ == "":
            answ = "Доступных username'ов нет!"
        else:
            answ = "Доступные username'ы:\n"+answ
    else:
        answ = "Доступные username'ы:\n"
        for i in range(len(channelarr)):
            answ += channelarr[i]+"\n"
    return answ


def check_session_name(name):
    for acc in my_apps:
        if name == acc.name:
            return False
    return True


def new_session_name():
    i = 0
    while True:
        name = 'account' + str(len(my_apps) + i)
        if check_session_name(name):
            return name
        else:
            i += 1


def success_login(message):
    global mode, id_user_registration
    print("Успешный вход!")
    id_user_registration = 0
    mode = 0
    message.reply('Вход выполнен успешно!')
    my_apps[-1].disconnect()
    my_apps[-1].start()
    my_apps[-1].send_message('me', 'Я в работе!')
    me = my_apps[-1].get_me()
    apps_data.append({
        'phone': me.phone_number,
        'username': me.username
    })
    save_accounts()

countcreatechannel = 0


def createchannel(name, id):
    global channelarr
    global iduserchannel
    global idapp
    global countcreatechannel
    try:
        countcreatechannel += 1
        if (countcreatechannel > 2):
            changeaccount()
            countcreatechannel = 0
        if len(channelarr) > len(my_apps)*16-1:
            mybot.send_message(
                id, "Бот переполнен! Невозможно зарезервировать " + name)
        else:
            my_apps[workacc].set_chat_username(
                my_apps[workacc].create_channel(name).id, name)

    except FloodWait as e:
        changeaccount()
        mybot.send_message(id, "Достигнут лимит! Ограничение на: " +
                           str(e.x)+" секунд! Включен аккаунт: " + str(workacc+1))
        createchannel(name, id)
        return
    except Exception as e:
        print(e)
        mybot.send_message(id, "Ошибка, меняю аккаунт!")
        changeaccount()
        time.sleep(5)
        createchannel(name, id)
        return
    else:
        channelarr.append(name)
        iduserchannel.append(id)
        idapp.append(workacc)
        mybot.send_message(id, "Username: " + name + " забронирован! Аккаунт: " + apps_data[workacc]['phone'])
        fl = False
    saveinfile(False)


def deletechanel(name, message):
    global idapp
    global channelarr
    global iduserchannel
    global countcreatechannel
    if name in channelarr:
        if message.chat.id == iduserchannel[channelarr.index(name)]:
            try:
                my_apps[idapp[channelarr.index(name)]].delete_channel(name)
            except FloodWait as e:
                changeaccount()
                message.reply("Достигнут лимит! Ожидайте: " + str(e.x) +
                              " секунд! Включен аккаунт: " + str(workacc+1))
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
        message.reply(
            "Username: " + message.text[9:] + " не найден в списке доступных username'ов!")


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
    now = -1

    while (asyncfl):
        time.sleep(59)
        available = False
        # now = int(datetime.now().hour)*60+int(datetime.now().minute)+3*60
        now = int(datetime.now().hour)*60+int(datetime.now().minute)
        for i in range(len(timereq)):
            if timereq[i] == now and firstreq:
                count = 0
                count2 = 0
                newiduserchannel = []
                print("Check!")
                firstreq = False
                for i in range(len(usernamearr)):
                    try:
                        count += 1
                        if my_apps[workacc].invoke(functions.account.CheckUsername(username=usernamearr[i])):
                            print('Свободен')
                            createchannel(usernamearr[i], idusersarr[i])
                            newiduserchannel.append(idusersarr[i])
                            usernamearr.remove(usernamearr[i])
                            idusersarr.remove(idusersarr[i])
                            saveinfile(True)
                            available = True
                            count2 += 1
                            count += 2
                        if count > 4:
                            changeaccount()
                            count = 0
                        if (count2 > len(my_apps)*2):
                            time.sleep(60-len(my_apps)*2)
                        time.sleep(1)
                    except UsernameInvalid:
                        if count > 4:
                            changeaccount()
                            count = 0
                        if (count2 > len(my_apps)*2):
                            time.sleep(60-len(my_apps)*2)
                        time.sleep(1)
                    except FloodWait as e:
                        fl = False
                        flo = False
                        i -= 1
                        changeaccount()
                        print("Достигнут лимит! Ограничение на: " + str(e.x) +
                              " секунд! Включен аккаунт: " + str(workacc+1))
                        sendallusers("Достигнут лимит! Ограничение на: " +
                                     str(e.x)+" секунд! Включен аккаунт: " + str(workacc+1))
                    except Exception as e:
                        print(e)
                        sendallusers("Произошла ошибка!")
                        i -= 1
                        changeaccount()
                if not available:
                    for user in users:
                        if not (user in newiduserchannel):
                            mybot.send_message(
                                user, "Произошел опрос юзернеймов, доступных не обнаруженно!")
            else:
                firstreq = True


openfromfile()


thread1 = Thread(target=follow, args=())
thread1.start()


print("Bot started!")


@mybot.on_message()
def hello(client, message):
    global fl, fl2, flo, svusername, usernamearr
    global asyncfl, intime, timereq, channelarr, idusersarr, password
    global mode, id_user_registration, code, phonehash, phonenumber, code, my_apps

    fl2 = False
    if message.chat.id in users:
        if id_user_registration == message.chat.id:
            if mode == 3:
                try:
                    my_apps[-1].check_password(message.text)
                except RPCError as e:
                    print(e)
                    message.reply(
                        "Ошибка входа! Чтобы начать с начала введите /add_account")
                    id_user_registration = 0
                    return
                else:
                    success_login(message)
                    return

            if mode == 2:
                try:
                    code = message.text[1:-1]
                    print(code)
                    my_apps[-1].sign_in(phone_number=phonenumber,
                                        phone_code_hash=phonehash, phone_code=code)
                except SessionPasswordNeeded:
                    message.reply("Введите пароль аккаунта")
                    mode += 1
                except Exception as e:
                    message.reply("Ошибка")
                    my_apps.pop(-1)
                    print(e)
                    mode = 0
                    id_user_registration = 0
                else:
                    success_login(message)
                    mode = 0
                    return
                return

            if mode == 1:
                my_apps.append(Client(new_session_name(), api_hash = api_hash, api_id = api_id))
                print('adding...')
                my_apps[-1].connect()
                phonenumber = message.text
                print("Телефон: " + phonenumber)
                try:
                    phonehash = (
                        (my_apps[-1].send_code(phonenumber))).phone_code_hash
                except Exception as e:
                    message.reply("Ошибка")
                    my_apps.pop(-1)
                    print(e)
                    mode = 0
                    id_user_registration = 0
                else:
                    message.reply(
                        "Введите код в формате 0ХХХХХ0, где ХХХХХ - одноразовый код")
                    mode += 1
                return

            if mode == 0 and message.text == "/add_account":
                mode = 1
                message.reply("Введите номер телефона аккаунта")
                id_user_registration = message.chat.id
                return
        else:
            if message.text == "/add_account":
                if id_user_registration == 0:
                    id_user_registration = message.chat.id
                    mode = 1
                    message.reply("Введите номер телефона аккаунта")
                else:
                    message.reply(
                        "Кто-то уже регистрируется! Пожалуйста подождите!")
                return

            if intime == message.chat.id:
                timereq = []
                intime = 0
                fl2 = True
                answ = message.text.split(' ')
                for i in range(0, len(answ), 1):
                    timereq.append(
                        (int(answ[i].split(':')[0]))*60+(int(answ[i].split(':')[1])))
                message.reply(listtime())

            if message.text.find("/start") != -1 or message.text == "/help":
                fl2 = True
                message.reply("Введите ‘Username’, чтобы забронировать его или начать отслеживать\nДля взаимодействия с ботом используйте следующие команды:\n/trackednames – список отслеживаемых username’ов\n/avaiblenames  – список «забронированных» username’ов\n/release – отменить «бронирование» username’а из списка\n/stop – остановить отслеживание username’а из списка\n/add_account – добавить новый аккаунт\n/help – список команд")
            if message.text == "/help_"+password:
                fl2 = True
                message.reply("Расширенные возможности:\n/time_" + password + " – установить время проверки username’ов\n/listall_"+password+" – список отслеживаемых username’ов\n/allavaiblenames_"+password +
                              "  – список «забронированных» username’ов\n/stopall_" + password + " – очистить список отслеживаемых username’ов\n/changeaccount – принудительно сменить рабочий аккаунт\n/changepassword_"+password+"_'новый_пароль' – установить новый пароль")

            if message.text.find("/changepassword_"+password) != -1:
                password = message.text[17+len(password):]
                fl2 = True
                message.reply("Новый пароль: " + str(password))

            if message.text == "/time_"+password:
                intime = message.chat.id
                fl2 = True
                message.reply(
                    "Введите время опроса в формате: ХХ:ХХ YY:YY ZZ:ZZ")

            if message.text == "/changeaccount":
                changeaccount()
                message.reply("Запущен " + str(workacc+1) + " аккаунт")
                fl2 = True

            if message.text.find("/stop_") != -1:
                fl2 = True
                try:
                    if idusersarr[usernamearr.index(message.text[6:].lower())] == message.chat.id:
                        idusersarr.pop(usernamearr.index(
                            message.text[6:].lower()))
                        usernamearr.remove(message.text[6:].lower())
                except Exception:
                    message.reply("Ошибка!")
                else:
                    saveinfile(True)
                    message.reply("Отслеживание " +
                                  message.text[6:] + " остановленно!\n")

            if message.text.find("/listall") != -1:
                fl2 = True
                message.reply("Отслеживается " + str(len(usernamearr)) +
                              " username'ов:\n" + listname(message.chat.id, message.text[9:]))

            if message.text.find("/stopall_" + password) != -1:
                fl2 = True
                usernamearr = []
                idusersarr = []
                message.reply(listname(message.chat.id, message.text[9:]))
                saveinfile(True)

            if message.text == "/stop":
                fl2 = True
                answ = ""
                for i in range(0, len(usernamearr), 1):
                    if message.chat.id == idusersarr[i]:
                        answ += "/stop_" + usernamearr[i]+"\n"
                if answ == "":
                    answ = "Нет отслеживаемых username'ов\n"
                message.reply(answ)

            if message.text == "/trackednames":
                fl2 = True
                message.reply(listname(message.chat.id, 0))

            if message.text == "/avaiblenames":
                fl2 = True
                message.reply(listchannel(message.chat.id, 0))

            if message.text == "/allavaiblenames_" + password:
                fl2 = True
                message.reply(listchannel(message.chat.id, password))

            if message.text.find("/release_") != -1:
                fl2 = True
                if (message.chat.id == iduserchannel[channelarr.index(message.text[9:])]):
                    deletechanel(message.text[9:].lower(), message)

            if message.text.find("/release") != -1 and not fl2:
                fl2 = True
                answ = ""
                for uname in channelarr:
                    if (message.chat.id == iduserchannel[channelarr.index(uname)]):
                        answ += "/release_" + uname + "\n"
                if answ == "":
                    answ = "Доступных username'ов нет!"
                else:
                    answ = "Выберите username:\n" + answ
                message.reply(answ)

            if message.text == "/botstop":
                fl2 = True
                print("Bot stoped!")
                asyncfl = False
                thread1.join()
                quit()

            if fl2 == False:
                svusername = message.text.lower()
                if svusername in usernamearr:
                    message.reply("Данный username уже отслеживается!")
                else:
                    try:
                        if my_apps[workacc].invoke(functions.account.CheckUsername(username=svusername)):
                            createchannel(svusername, message.chat.id)
                        else:
                            usernamearr.append(svusername)
                            idusersarr.append(message.chat.id)
                            message.reply(
                                "Отслеживание " + svusername + " запущено!\nОтслеживаемые username'ы: /trackednames")
                            saveinfile(True)
                    except FloodWait as e:
                        fl = False
                        flo = False
                        changeaccount()
                        print("Достигнут лимит! Ограничение на: " + str(e.x) +
                              " секунд! Включен аккаунт: " + str(workacc+1))
                        message.reply("Достигнут лимит! Ограничение на: " +
                                      str(e.x)+" секунд! Включен аккаунт: " + str(workacc+1))
                    except UsernameInvalid:
                        usernamearr.append(svusername)
                        idusersarr.append(message.chat.id)
                        saveinfile(True)
                        message.reply("Некорректный или заблокированный username!\nОтслеживание " +
                                      svusername + " запущено!\nОтслеживаемые username'ы: /trackednames")
    else:
        if message.text == "/start_"+tokken:
            saveusers(message.chat.id)
            message.reply("Введите ‘Username’, чтобы забронировать его или начать отслеживать\nДля взаимодействия с ботом используйте следующие команды:\n/trackednames – список отслеживаемых username’ов\n/avaiblenames  – список «забронированных» username’ов\n/release – отменить «бронирование» username’а из списка\n/stop – остановить отслеживание username’а из списка\n/add_account – добавить новый аккаунт\n/help – список команд")


mybot.start()
for app in my_apps:
    app.start()
    me = app.get_me()
    apps_data.append({
        'phone': me.phone_number,
        'username': me.username
    })
idle()

mybot.stop()
for app in my_apps:
    app.stop()
