import telebot
import datetime
import schedule
import pickle

from time import sleep
from threading import Thread
from telebot.apihelper import ApiTelegramException

FILE = 'log.txt'


def logprint(s: str):
    """Выводит print в FILE. Проверяет длину файла. Если она больше 999, убирает половину.

    Parameters:
        s: строка, которую надо вывести"""

    with open(FILE, 'a+') as fa:
        print(str(datetime.datetime.now()) + ' ' + s, file=fa)
        if fa.read().count('\n') == 999:
            lines = fa.read[len(fa.read()) / 2:]
            with open(FILE, 'w') as fw:
                fw.write(lines)


class TeleBoolichka:
    def __init__(self, google_api):
        self.token = None  # Токен бота
        #self.token = None # Тестовый токен
        self.GoogleApi = google_api  # Экземпляр класса GoogleFormsApi

    def spam(self) -> [str]:
        """Создает Alert-сообщение для формы на организаторов"""

        # Количество ответов в форме за сутки
        ans = self.GoogleApi.new_answers(0)
        if ans > 0:
            msg = f'\[ALERT] Форму на организаторов заполнили {ans} человек:\n\n\n'
            self.GoogleApi.upload(0)
            for i in range(ans):
                response = self.GoogleApi.get_response(i, True)
                info = identify(response, self.GoogleApi.FormsId[0])
                msg += f'_{info["Время"]}_\n*{info["ФИО"]}*\n' \
                       f'*ВУЗ* - {info["ВУЗ"]}\n*Факультет* - {info["Факультет"]}\n*Курс* - {info["Курс"]}.\n' \
                       f'*ВК* - {info["ВК"]}\n*Почта* - {info["Почта"]}\n\n'
            return msg
        else:
            return -1


def identify(response, form_id=0):
    """ Возвращает ответы с формы в нужном формате для сообщения.
     keys - ФИО, ВУЗ, Факультет, Курс, Почта, ВК, Время"""

    form_Q = pickle.load(open('FormsQuestions.pickle', 'rb'))[form_id]
    person = {'Время': response['createTime'][:-5].replace('T', ' ')}
    response = response['answers']

    for key in form_Q.keys():
        if form_Q[key] in response.keys():
            person[key] = response[form_Q[key]
                                   ]['textAnswers']['answers'][0]['value']
    return person


def schedule_checker():
    """Проверяет наступило ли необходимое время для вызова функции по расписанию."""
    while True:
        schedule.run_pending()
        sleep(1)


def run(Forms):
    """Главная функция

    Parameters:
        Forms: экземпляр класса GoogleFormsApi"""

    logprint('Bot started')
    botlogic = TeleBoolichka(Forms)
    bot = telebot.TeleBot(botlogic.token)

    @bot.message_handler(commands=['start'])
    def welcome(message):
        logprint(f'/start {message.chat.id}')
        bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

    @bot.message_handler(commands=['help'])
    def help_message(message):
        bot.send_message(message.chat.id,
                         '''Список комманд, доступных тебе:
                         \n/alarm - подписаться на уведомления от бота 
                         (заявки из формы на организаторов, 12:00 ежедневно)
                         \n/cancel - отписаться от уведомлений''')

    @bot.message_handler(commands=['alarm', 'alarms'])
    def alarm(message):
        logprint(f'/alarm {message.chat.id}')

        ids = pickle.load(open('Chat_ids.pickle', 'rb'))
        if message.chat.id not in ids:
            ids.add(message.chat.id)
            pickle.dump(set(ids), open('Chat_ids.pickle', 'wb'))
            bot.send_message(message.chat.id, 'Вы подписались на рассылку')
        else:
            bot.send_message(message.chat.id, 'Вы уже подписаны на рассылку')

    @bot.message_handler(commands=['cancel', 'unalarm'])
    def unalarm(message):
        logprint(f'/unalarm {message.chat.id}')
        ids = pickle.load(open('Chat_ids.pickle', 'rb'))
        if message.chat.id not in ids:
            bot.send_message(message.chat.id, 'Вы не подписаны на рассылку')
        else:
            ids.remove(message.chat.id)
            pickle.dump(set(ids), open('Chat_ids.pickle', 'wb'))
            bot.send_message(message.chat.id, 'Вы отписались от рассылки')

    def send_alarm():
        """Отправляет сообщение и обрабатывает ошибки при отправке."""
        logprint('Spam process is started')
        ids_to_spam = pickle.load(open('Chat_ids.pickle', 'rb'))
        for i in ids_to_spam:
            try:
                spam = botlogic.spam()
                if spam != -1:
                    bot.send_message(i, spam, parse_mode='Markdown')
                else:
                    logprint('Not any spam')
                    break
            except ApiTelegramException as e:

                logprint(e)
                logprint(type(str(e)))
                if e.error_code == 403:
                    logprint('User blocked bot')
                    ids = pickle.load(open('Chat_ids.pickle', 'rb'))
                    ids.remove(i)
                    pickle.dump(set(ids), open('Chat_ids.pickle', 'wb'))

                    ids = pickle.load(open('ErrorUsers.pickle', 'rb'))
                    ids.add(i)
                    pickle.dump(ids, open('ErrorUsers.pickle', 'wb'))
                if 'is too long' in str(e):
                    logprint('Msg is too long')
                    spam1 = spam[:len(spam) // 2] + "\nСообщение слишком длинное. Чтобы посмотреть другие ответы" \
                                                    " откройте форму вручную"
                    try:
                        bot.send_message(i, spam1, parse_mode='Markdown')
                    except:
                        logprint('There was super error')
                        ids = pickle.load(open('Chat_ids.pickle', 'rb'))
                        ids.remove(i)
                        pickle.dump(set(ids), open('Chat_ids.pickle', 'wb'))

                        ids = pickle.load(open('ErrorUsers.pickle', 'rb'))
                        ids.add(i)
                        pickle.dump(ids, open('ErrorUsers.pickle', 'wb'))
            except Exception as e:
                logprint('Internal error')

    schedule.every().day.at("12:00").do(send_alarm)
    #schedule.every(20).seconds.do(send_alarm)
    Thread(target=schedule_checker).start()

    bot.infinity_polling(timeout=10, long_polling_timeout=5)
