import datetime
from response_script import *
from json_handler import *
import schedule


# плановый запуск проверки событий
def job():
    print('Проверка выполнена')
    # main()
    print(get_info('answer.json'))
    print(datetime.datetime.now())


schedule.every(3).seconds.do(job)

while True:
    schedule.run_pending()
