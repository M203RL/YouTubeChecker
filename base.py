from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json
from autoPost import post, initial
import pyperclip
import time

# Replace with your API key
API_KEY = ''

def get_public_videos(channelID, test = False):
    current_dateTime = datetime.now()
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
        maxResults=1  # You can change this to get more results
    )
    
    video_response = video_request.execute()
    # Retrieve the first video details
    first_video = video_response['items'][0]['snippet']
    videoID = first_video['resourceId']['videoId']
    link = f'https://www.youtube.com/watch?v={videoID}'

    publish_time = first_video['publishedAt']
    publish_datetime = datetime.fromisoformat(publish_time[:-1])

    title = first_video['title']
    
    description = first_video['description']
    skip_word = "\n\n——"
    description = description[ 0 : description.index(skip_word)]

    if (publish_datetime.year, publish_datetime.month, publish_datetime.day) == {current_dateTime.year, current_dateTime.month, current_dateTime.day} or test:
        if (publish_datetime.hour == 11 and publish_datetime.minute >= 58) or (publish_datetime.hour == 12 and publish_datetime.minute <= 2) or test:
            return {'title': title, 'link': link, 'description': description}
    
    print(f"Title: {title}\nDescription: {description}\nPublished At: {publish_time}\nLink:{link}")
    

if  __name__ == '__main__':
    test = False
    test = True

    timer = False
    timer = True
    ## 前文
    pre_text = ''
    ##Time Set
    (hs, ms, ss)=(12, 0, 0)

    t = time.localtime()
    year=int(time.strftime('%y',t))
    month=int(time.strftime('%m',t))

    result = time.strftime("%Y/%m/%d %H:%M:%S", t)
    print(f"Start Time: {result}")
    animation = "|/—\\"
    ix = 0
    hour=int(time.strftime('%H',t))
    min=int(time.strftime('%M',t))
    sec=int(time.strftime('%S',t))
    day = datetime.datetime.today().weekday()
    if timer or test:
        while hour!=hs or min!=ms or sec<=ss:
            ds = (hs-hour)*60*60+(ms-min)*60+(ss-sec)
            resultTime = datetime.timedelta(seconds = ds)
            print(f' {animation[round(ix*0.25) % len(animation)]}T-{resultTime}         ',end='\r')
            ix+=1
            time.sleep(0.001)
            t = time.localtime()
            hour=int(time.strftime('%H',t))
            min=int(time.strftime('%M',t))
            sec=int(time.strftime('%S',t))
            day = datetime.datetime.today().weekday()
        time.sleep(1)

    driver = initial(test)
    video_json = {}
    text = ''
    title = ''


    with open('./Data/channel.json', 'r', encoding='utf-8') as f:
        channel_info = json.load(f)
    with open('./Data/FirstVideo.json', 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4, ensure_ascii=False) 
    
    
    text += f'[div align=left][size=4][b]{pre_text}[/b][/size][/div]\n'
    for channel in list(channel_info.keys()):
        channelID = channel_info[f'{channel}']
        video_json[f'{channel}'] = get_public_videos(channelID, test)
        video_title = video_json[f'{channel}']['title']
        video_link = video_json[f'{channel}']['link']
        video_description = video_json[f'{channel}']['description']
        with open('./Data/FirstVideo.json', 'w', encoding='utf-8') as f:
            json.dump(video_json, f, indent=4, ensure_ascii=False)
        
        text += f'[movie={video_link} width=640 height=360][/div]'
        text += f'[div align=left][size=3][b]{video_description}[/b][/size][/div]\n\n'
    pyperclip.copy(text)
    
    if title == '':
        title = 'Undefined Title'
    myLink = post(driver, test, title, text)



