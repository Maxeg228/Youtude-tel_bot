import json
import datetime
from googleapiclient.discovery import build
from db_work import search_ch


def video_rating(video_id):
    with open('CLIENT_SECRET_FILE.json') as client_secret_file:
        client_data = json.load(client_secret_file)  # получение данных из файла с данными разработчика

    youtube = build('youtube', 'v3', developerKey=client_data['key'])
    rating_req = youtube.videos().list(
        part="statistics",
        id=video_id
    )
    res = rating_req.execute()
    return res['items'][0]['statistics']


def channelid_response(name_list, it_is_db=True):  # запрос id каннала по его имени
    with open('CLIENT_SECRET_FILE.json') as client_secret_file:
        client_data = json.load(client_secret_file)  # получение данных из файла с данными разработчика

    youtube = build('youtube', 'v3', developerKey=client_data['key'])
    if it_is_db:
        channels = search_ch()
        channels_id = []
        for channel in channels:
            channel = channel.split(';')
            for elem in channel:
                print(elem)
                if len(elem) == 24 and elem[0] == 'U':
                    channels_id.append(elem)
                else:
                    id_request = youtube.channels().list(
                        part='id',
                        forUsername=elem.strip())
                    res_id = id_request.execute()
                    try:
                        if res_id['items'][0]['id'] not in channels_id:
                            channels_id.append(res_id['items'][0]['id'])
                            print(res_id['items'][0]['id'], '12')
                    except Exception as ex:
                        print(ex)
        return channels_id

    id_request = youtube.channels().list(
        part='id',
        forUsername=name_list)
    res_id = id_request.execute()
    channels_id = []
    try:
        print(res_id['items'][0]['id'])
        if res_id['items'][0]['id'] not in channels_id and res_id['items'][0]['id']:
            channels_id.append(res_id['items'][0]['id'])
    except Exception as ex:
        print(ex)
    if channels_id:
        return channels_id[0]
    else:
        return 0


def main_response(channels_id):  # запрос событий по списку id канналов
    with open('CLIENT_SECRET_FILE.json') as client_secret_file:
        client_data = json.load(client_secret_file)  # получение данных из файла с данными разработчика
    print(channels_id)
    youtube = build('youtube', 'v3', developerKey=client_data['key'])

    # составление запроса
    requests = []
    for elem in channels_id:
        requests.append(youtube.activities().list(
            part='snippet',
            channelId=elem,
            publishedAfter=(datetime.datetime.now()

                            - datetime.timedelta(hours=600)).replace(tzinfo=datetime.timezone.utc).isoformat()))
    result = []
    for elem in requests:
        result.append(elem.execute())
    to_write = []

    for res in result:
        try:
            to_write.append(res['items'])
        except Exception as ex:
            print(ex)

    with open('answer.json', mode='w') as answer_file:
        json.dump(to_write, answer_file)
    print('Запрос выполнен и записан в answer.json')

