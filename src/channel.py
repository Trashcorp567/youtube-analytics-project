import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб - канала"""

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API.
        """
        self.channel_id = channel_id
        self.title = ""
        self.description = ""
        self.url = ""
        self.subscriber_count = 0
        self.video_count = 0
        self.view_count = 0
        self.fetch_channel_data()

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def to_json(self, filename: str):
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filename, 'w') as file:
            json.dump(data, file)

    def fetch_channel_data(self):
        youtube = self.get_service()
        channel = youtube.channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()

        if 'items' in channel:
            channel_data = channel['items'][0]
            snippet = channel_data['snippet']
            statistics = channel_data['statistics']

            self.title = snippet['title']
            self.description = snippet['description']
            self.url = f"https://www.youtube.com/channel/{self.channel_id}"
            self.subscriber_count = int(statistics['subscriberCount'])
            self.video_count = int(statistics['videoCount'])
            self.view_count = int(statistics['viewCount'])

    @classmethod
    def get_service(cls):
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = self.get_service()
        channel = youtube.channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()
        print(json.dumps(channel, indent = 2, ensure_ascii = False))