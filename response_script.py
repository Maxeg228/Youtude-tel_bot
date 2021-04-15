import json
import datetime
from googleapiclient.discovery import build
from db_work import search_ch


def channelid_response(name_list, it_is_db=True):
    with open('CLIENT_SECRET_FILE.json') as client_secret_file:
        client_data = json.load(client_secret_file)  # получение данных из файла с данными разработчика

    youtube = build('youtube', 'v3', developerKey=client_data['key'])
    channels = search_ch()
    channels_id = []
    for channel in channels:
        channel = channel.split(';')
        for elem in channel:
            print(elem)
            id_request = youtube.channels().list(
                part='id',
                forUsername=elem)
            res_id = id_request.execute()
            # print(res_id)
            try:
                if res_id['items'][0]['id'] not in channels_id:
                    channels_id.append(res_id['items'][0]['id'])
            except Exception:
                pass
    return channels_id


def main_response(channels_id):
    with open('CLIENT_SECRET_FILE.json') as client_secret_file:
        client_data = json.load(client_secret_file)  # получение данных из файла с данными разработчика

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
        except Exception:
            pass

    with open('answer.json', mode='w') as answer_file:
        json.dump(to_write, answer_file)


if __name__ == '__main__':
    main_response(channelid_response('CLIENT_SECRET_FILE.json'))
