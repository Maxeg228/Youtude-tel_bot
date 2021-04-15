import json
import time

from telegram import bot
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from db_work import add_info, del_info, search_id
from response_script import channelid_response

with open('CLIENT_SECRET_FILE.json') as client_secret_file:
    client_data = json.load(client_secret_file)
TOKEN = client_data['telegram_token']


def start(update, context):
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!")


def help(update, context):
    update.message.reply_text(
        "/add_channel - Добавить канал;\n"
        "/del_channel - Убрать канал из списка отслеживаемых")


# TODO
# @bot.message_handler(commands=["Newsletter"])
# def answer(message):
#     newsletter = message.text.split(maxsplit=1)[1]
#     id_list = search_id()
#     for i in range(len(id_list)):
#         try:
#             time.sleep(5)
#             bot.send_message(id_list[i]['id'], newsletter)
#         except:
#             continue

def ans(update, context):
    update.message.sendMessage(chat_id=1153144266, text='Hello, World')


def add_channel(update, context):
    correct = True
    try:
        user_id = update.message.from_user.id
        add_info(user_id, update.message.text[13::])
    except Exception as ex:
        print(ex)
        correct = False
        update.message.reply_text('Произошла ошибка повторите команду.')
    if correct:
        update.message.reply_text('Канал добавлен.')
    # update.user.id()


def del_channel(update, context):
    user_id = update.message.from_user.id
    del_info(user_id, update.message.text)
    update.message.reply_text('Канал удалён')


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("test", ans))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("add_channel", add_channel))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
