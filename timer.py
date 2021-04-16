import datetime
from response_script import *
from json_handler import *
from telegram_bot import *
from db_work import search_id
import schedule


# плановый запуск проверки событий
def job():
    print('Проверка выполнена')
    # main_response(channelid_response('CLIENT_SECRET_FILE.json'))

    telegram_bot_sendtext(get_info('answer.json'), search_id())

    # print(get_info('answer.json'), sep='\n')
    print(datetime.datetime.now())


schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
