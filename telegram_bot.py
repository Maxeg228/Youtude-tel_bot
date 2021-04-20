import json

import requests
from telegram.ext import Updater
from telegram.ext import CommandHandler
from db_work import add_info, del_info, search_user_channels
from response_script import channelid_response

with open('CLIENT_SECRET_FILE.json') as client_secret_file:
    client_data = json.load(client_secret_file)
TOKEN = client_data['telegram_token']


def start(update, context):
    update.message.reply_text(
        "Привет! Что-бы добавить канал напиши\n"
        "/add_channel 'название канала'\n"
        "Где взять название канала:\n"
        "https://www.youtube.com/c/'Вот здесь'/videos")


def helpt(update, context):
    update.message.reply_text(
        "/add_channel - Добавить канал;\n"
        "/del_channel - Убрать канал из списка отслеживаемых")


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
    del_info(user_id, update.message.text[13::])
    if update.message.text[13::].strip() == '' or update.message.text[13::].strip() == 'all':
        update.message.reply_text('пользователь очищен')
    else:
        update.message.reply_text('Канал удалён')


def telegram_bot_sendtext(bot_message, botid_list):  # функция рассылки
    bot_token = TOKEN
    text_for_user = []
    for bot_chatID in botid_list:
        check_list = list(map(lambda x: channelid_response(x, it_is_db=False), search_user_channels(bot_chatID)))
        for massage in bot_message:
            if massage[0].strip() in check_list:
                print()
                cor_massage = ' \n '.join(massage[1::])
                print(cor_massage)
                try:
                    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(bot_chatID) \
                                + '&parse_mode=Markdown&text=' + cor_massage
                except Exception as ex:
                    print(ex)
                text_for_user.append(send_text)
    print(text_for_user)
    for elem in text_for_user:
        response = requests.get(elem)
    return response.json()


def good_morning(botid_list):
    bot_token = TOKEN
    text_for_user = []
    for bot_chatID in botid_list:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(bot_chatID) \
                    + '&parse_mode=Markdown&text=' + "Доброе утро, варите кофе, смотрите видео и хорошего вам дня"

        text_for_user.append(send_text)
    for elem in text_for_user:
        response = requests.get(elem)
    return response.json()


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpt))
    dp.add_handler(CommandHandler("add_channel", add_channel))
    dp.add_handler(CommandHandler("del_channel", del_channel))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
