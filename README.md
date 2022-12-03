#                ![avatar](https://sun1-13.userapi.com/s/v1/ig2/1r0-byxqFwdntyCx2i6Cxc7zn4yTw9oRDkcLqX789qs6OY9_IBqz2P08wtzp6K35BK9K_cJ-MtI9TyCBczcNCIWF.jpg?size=50x50&amp;quality=96&amp;crop=176,90,541,541&amp;ava=1)                                                    Телеграм Бот Алертер                             

Название            | Содержание
----------------    |----------------------
main.py             | главный скрипт запуска работы бота
Boolichka.py        | скрипт с логикой бота
GoogleForm.py       | скрипт с подключением к Google Forms API
ErrorUsers.pickle   | pickle-файл с id пользователей, которым не приходят сообщения от бота
FormsQuestions.pickle | pickle-файл с id форм и id вопросов форм, используемых для формирования алертов
Uploaded.pickle       | pickle-файл с временным хранением формы для сокращения запросов к API
client_secrets.json   | json-файл с мета-данными для подключения к Google Forms API
token.json            | json-файл с мета-данными для подключения к Google Forms API

##                                                                    Описание

Телеграм бот REU Data Science Club, который интегрируется с Google Forms API и присылает оповещения каждый раз, когда та или иная форма клуба заполнена.
Подписаться на уведомления от бота: https://t.me/DSClubAlerterBot


##                                                                    Документация

  [Документация по работе с Google Forms API](https://developers.google.com/forms/api)
  
  [Документация по работе telebot](https://pypi.org/project/pyTelegramBotAPI/)
  
  [Документация по работе с текущей реализацией Телеграм бота](https://www.notion.so/37898df74f7448ada6cdd94aebd6f393)
  
##                                                                    Дополнительно
###                                                                   Зависимости

  Для настройки необходимых пакетов python для запуска скрипта введите в командной строке:
  `pip install -r "requirements.txt"`
  
  Для запуска бота на хостинге vds.ru и перевод запуска в фоновый процесс:
  
  
  1. Введите `ssh 194.87.145.32 -l root`
  2. Введите пароль
  3. Введите `python3 main.py --noauth_local_webserver 2>>log.txt`
  4. Введите `disown -h %N` (где `N` - номер запущенного процесса, `ps` - команда для вывода процессов и их id)
  Если необходимо процесс перевести в активный `fg %N`
  Если необходимо убить процесс` kill -kill N`
  
  
  
  
  
###                                                                    Контакты


  **Telegram**: @seelova, @Boombotts, @vitykos \
  **VK**: vk.com/seelova, vk.com/boomsbott, vk.com/vitykos \
  
  
