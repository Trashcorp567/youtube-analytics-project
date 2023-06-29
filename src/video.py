import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.title = None
        self.video_url = None
        self.like_count = None
        self.view_count = None
        self.comment_count = None
        self.fetch_video_data()

    def __str__(self):
        return self.title

    @staticmethod
    def get_service():
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def fetch_video_data(self):
        try:
            youtube = self.get_service()
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=self.video_id
                                                   ).execute()

            self.title: str = video_response['items'][0]['snippet']['title']
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
            self.comment_count: int = video_response['items'][0]['statistics']['commentCount']
            self.video_url: str = f"https://www.youtube.com/watch?v={self.video_id}"

        except:
            self.title = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None
            self.video_url = None
            #print(f'Неправильное id: {self.video_id}')


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return self.title
