import json


# Обработка полученного json файла и поддготовка данных к отправке

def get_info(file_json):
    mailing_info = []
    with open(file_json) as answer:
        data = json.load(answer)
    for elem in data:
        if elem:
            for activity in elem:
                if activity['snippet']['type'] == 'upload':
                    mailing_info.append(
                        [activity['snippet']['channelTitle'], activity['snippet']['title'], activity['id']])
    return mailing_info


if __name__ == '__main__':
    print(*get_info('answer.json'), sep='\n')
