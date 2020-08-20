from private_token import token, chat_id
import requests
import telebot
import database
from threading import Thread, Event
import time

bot = telebot.TeleBot(token)
deleted_flag = True


def generate_new_chat_link():
    r = requests.get("https://api.telegram.org/bot" + token + "/exportChatInviteLink", params={'chat_id': chat_id})
    if not r.json()['ok']:
        return "<Some error, can't generate link, please try again>"

    return r.json()['result']


chat_link = generate_new_chat_link()


def check_premium():
    try:
        current_time = int(time.time())
        users = database.deleted_users(current_time)
        for user in users:
            kick_user(user[0])

        database.remove(current_time)

    except Exception as e:
        print(e)


class TimerThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(300):
            if not deleted_flag:
                continue

            global chat_link
            chat_link = generate_new_chat_link()
            check_premium()


stopEvent = Event()
thread = TimerThread(stopEvent)
thread.start()


def kick_user(user_id):
    if user_id is None:
        return

    r = requests.get("https://api.telegram.org/bot" + token + "/kickChatMember", params={'chat_id': chat_id, 'user_id': user_id})
    if not r.json()['ok']:
        print("Can't kick user " + str(user_id))
        print(r.json()['description'])


@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.id < 0:
        return

    global deleted_flag
    deleted_flag = False

    args = message.text.split(' ')
    if len(args) != 2:
        bot.send_message(message.chat.id, 'Неправильные аргументы при запуске бота. Пожалуйста, '
                                          'перейдите по выданной Вам ссылке.')
        return

    try:
        if database.in_database(args[1], message.from_user.id):
            database.update_user_data(args[1], message.from_user.id)
            bot.send_message(message.chat.id, 'Здравствуйте!. Вот ссылка на премиум-чат: ' + chat_link + '\n'
                             + 'Обратите внимание, что ссылка меняется каждые 5 минут. '
                               'Если ссылка оказалось недействительной, '
                               'то введите команду /start ещё раз')
        else:
            bot.send_message(message.chat.id, 'Здравствуйте! Извините, но к сожалению я не могу добавить Вас в чат, '
                                              'так как у Вас нет премиум-доступа.')
    except Exception as e:
        print(e)

    deleted_flag = True


@bot.message_handler(content_types=['new_chat_members'])
def handle_new_member(message):
    global deleted_flag
    deleted_flag = False
    try:
        for user in message.new_chat_members:
            if not database.in_database(user.id):
                kick_user(user.id)

    except Exception as e:
        print(e)

    deleted_flag = True


while True:
   try:
        bot.polling(none_stop=True)
   except Exception as e:
       print(e)
       time.sleep(10)

