from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Replace with your API key and the channel ID
API_KEY = ''
CHANNEL_ID = ''

def get_public_videos(channelID):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    # First, get the upload playlist ID
    channel_response = youtube.channels().list(
        part='contentDetails',
        id=channelID
    ).execute()
    
    upload_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    # Then, get the videos from the upload playlist
    video_request = youtube.playlistItems().list(
        part='snippet',
        playlistId=upload_playlist_id,
        maxResults=5  # You can change this to get more results
    )
    
    video_response = video_request.execute()
    
    videos = video_response.get('items', [])
    for video in videos:
        video_id = video['snippet']['resourceId']['videoId']
        title = video['snippet']['title']
        publish_time = video['snippet']['publishedAt']
        print(f"Title: {title}\nVideo ID: {video_id}\nPublished At: {publish_time}\n")
    
get_public_videos(CHANNEL_ID)
