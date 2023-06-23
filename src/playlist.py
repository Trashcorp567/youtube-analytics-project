from googleapiclient.discovery import build
from datetime import timedelta
import isodate
import os


class PlayList:
    def __init__(self, playlist_id):
        self.youtube = self.get_service()
        self.playlist_id = playlist_id
        self.title = ""
        self.url = ""
        self.fetch_playlist_data()

    @staticmethod
    def get_service():
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def total_duration(self):
        """
        Возвращает общую длительность всех видео в плейлисте
        """
        playlist_videos = self.youtube.playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails',
            maxResults=50,
        ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)
        ).execute()

        durations = []

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            durations.append(duration)

        total_duration = sum(durations, timedelta())
        return total_duration

    def fetch_playlist_data(self):
        """
        Вытаскивает информацию по плейлисту
        """
        playlist = self.youtube.playlists().list(
            id=self.playlist_id,
            part='snippet'
        ).execute()

        self.title = playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def show_best_video(self):
        """
        Возвращает самое популярное видео на основе количества лайков
        """
        playlist_items = self.youtube.playlistItems().list(
            playlistId=self.playlist_id,
            part='snippet',
            maxResults=50
        ).execute()

        best_video = None
        max_likes = 0

        for item in playlist_items['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video = self.youtube.videos().list(
                id=video_id,
                part='statistics'
            ).execute()
            video_likes = int(video['items'][0]['statistics']['likeCount'])

            if video_likes > max_likes:
                best_video = video_id
                max_likes = video_likes

        return f"https://youtu.be/{best_video}"
