import os
from dotenv import load_dotenv
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

yt_api_key = os.getenv('YT_API_KEY')
yt_client_secrets_file = os.getenv('YT_CLIENT_SECRETS_FILE')
scopes = ['https://www.googleapis.com/auth/youtube']

def get_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(yt_client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
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

def get_video_id(youtube, track_name):
    request = youtube.search().list(
        part='snippet',
        q=track_name,
        type='video',
        maxResults=1
    )
    response = request.execute()
    return response['items'][0]['id']['videoId']

def create_playlist_with_tracks(track_names):
    playlist_name = "Spotify copy"
    playlist_description = "description"
    try:
        youtube = get_service()

        video_ids = []
        for track_name in track_names:
            video_id = get_video_id(youtube, track_name)
            video_ids.append(video_id)

        playlist_id = create_playlist(youtube=youtube, title=playlist_name, description=playlist_description, privacy_status="public")

        for video_id in video_ids:
            add_video_to_playlist(youtube=youtube, playlist_id=playlist_id, video_id=video_id)

    except HttpError as e:
        print("An HTTP error occurred: %s" % e)

@app.route('/', methods=['POST'])
def upload_tracks():
    data = request.json
    track_names = data.get('trackNames', [])
    print("YouTube API Key:", yt_api_key)
    print("YouTube Client Secrets File Path:", yt_client_secrets_file)
    print("Received track names:", track_names)
    create_playlist_with_tracks(track_names)
    return jsonify({"status": "success", "trackNames": track_names})

if __name__ == '__main__':
    app.run(port=3000)
