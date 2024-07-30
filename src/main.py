import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

spotify_client_id = os.getenv('SPOTIFU_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

yt_api_key = os.getenv('YT_API_KEY')
yt_client_secrets_file = os.getenv('YT_CLIENT_SECRETS_FILE')
scopes = ['https://www.googleapis.com/auth/youtube']

# Demo; replace with info taken from spotify
track_names = ["Me and the Birds by Duster", "The Perfect Girl by Mareux", "Somebody That I Used to Know by Gotye", "Sphere by Creo"]
playlist_name = "Test Playlist"
playlist_description = "Test Description"

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(yt_client_secrets_file, scopes)
    credentials = flow.run_local_server()
    return build('youtube', 'v3', credentials=credentials)

def add_video_to_playlist(youtube, playlist_id, video_id):
    request_body = {
        'snippet': {
            'playlistId': playlist_id,
            'resourceId': {
                'kind': 'youtube#video',
                'videoId': video_id
            }
        }
    }

    request = youtube.playlistItems().insert(
        part='snippet',
        body=request_body
    )
    request.execute()

def create_playlist(youtube, title, description, privacy_status):
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }
    request = youtube.playlists().insert(
        part='snippet,status',
        body=request_body
    )

    response = request.execute()
    return response['id']

def get_video_id(track_name):
  request = youtube.search().list(
      part = 'snippet',
      q=track_name,
      type='video',
      maxResults=1
  )
  response = request.execute()
  return response['items'][0]['id']['videoId']

# Create a playlist given spotify tracks
try:
    youtube = get_service()

    video_ids = []

    # Find the first youtube video that shares its name with the spotify track
    for track_name in track_names:
        video_id = get_video_id(track_name)
        video_ids.append(video_id)

    playlist_id = create_playlist(youtube=youtube, title=playlist_name, description=playlist_description, privacy_status="public")

    # Add videos to playlist
    for video_id in video_ids:
        add_video_to_playlist(youtube=youtube, playlist_id=playlist_id, video_id=video_id)

except HttpError:
    print("Rate Limit Exceeded. Please try again later.")
