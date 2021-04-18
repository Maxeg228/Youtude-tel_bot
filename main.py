# Здесь происходит запуск рассылки и бота двумя процессами одновременно

from threading import Thread
from timer import start
from telegram_bot import main

process_bot = Thread(target=main)
process_start = Thread(target=start)

process_start.start()
process_bot.start()
