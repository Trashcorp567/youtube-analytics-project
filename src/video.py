import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.video_title = ""
        self.video_url = ""
        self.likes_count = ""
        self.view_count = 0
        self.fetch_video_data()

    def __str__(self):
        return self.video_title

    @staticmethod
    def get_service():
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def fetch_video_data(self):
        youtube = self.get_service()
        video = youtube.videos().list(
            part='snippet,statistics',
            id=self.video_id
        ).execute()

        if 'items' in video:
            video_data = video['items'][0]
            snippet = video_data['snippet']
            statistics = video_data['statistics']

            self.video_title = snippet['title']
            self.video_url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.view_count = int(statistics['viewCount'])
            self.likes_count = int(statistics['likeCount'])


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return self.video_title
