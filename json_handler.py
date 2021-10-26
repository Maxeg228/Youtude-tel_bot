import json
from response_script import video_rating


# Обработка полученного json файла и поддготовка данных к отправке

def get_info(file_json):
    mailing_info = []
    with open(file_json) as answer:
        data = json.load(answer)
    for elem in data:
        if elem:
            for activity in elem:
                if activity['snippet']['type'] == 'upload':
                    id_video = activity['snippet']['thumbnails']['default']['url'].split('/')[-2]
                    channel_id = activity['snippet']['channelId']
                    mailing_info.append(
                        [f'{channel_id}',
                         f'На каннале "{activity["snippet"]["channelTitle"]}"'
                         f' {activity["snippet"]["publishedAt"][:10:]} в '
                         f'{activity["snippet"]["publishedAt"][11:-6:]} вышло новое видео.',
                         activity['snippet']['title'],
                         f'https://www.youtube.com/watch?v={id_video}',
                         f'Просмотры - {video_rating(id_video)["viewCount"]}',
                         f'👍 - {video_rating(id_video)["likeCount"]}',
                         f'👎- {video_rating(id_video)["dislikeCount"]}'])

    return mailing_info
