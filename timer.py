from response_script import *
from json_handler import *
from telegram_bot import *
from db_work import search_id
import schedule
import datetime


# плановый запуск проверки событий
def job():
    print('Проверка выполнена')
    main_response(channelid_response('CLIENT_SECRET_FILE.json'))
    telegram_bot_sendtext(get_info('answer.json'), search_id())
    if datetime.datetime.now().time().hour in [7, 8, 9]:
        good_morning(search_id())


schedule.every(3 * 3).seconds.do(job)


def start():
    while True:
        schedule.run_pending()
