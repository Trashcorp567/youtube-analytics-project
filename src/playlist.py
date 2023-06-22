from src.channel import Channel
from datetime import timedelta
import isodate
import datetime


class PlayList(Channel):
    def __init__(self, playlist_id):
        super().__init__(channel_id='UC-OVMPlMA3-YCIeg4z5z23A')
        self.youtube = self.get_service()
        self.playlist_id = playlist_id
        self.playlists = self.youtube.playlists().list(
            channelId='UC-OVMPlMA3-YCIeg4z5z23A',
            part='contentDetails,snippet',
            maxResults=50,
        ).execute()
        self.fetch_playlist_data()

    @property
    def total_duration(self):
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
        for playlist in self.playlists['items']:
            if playlist['id'] == self.playlist_id:
                self.title = playlist['snippet']['title']
                self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def show_best_video(self):
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
            best_video = video_id

        return f"https://youtu.be/{best_video}"
