import csv
from googleapiclient.discovery import build
from collections import Counter
import streamlit as st
from Senti import extract_video_id
from googleapiclient.errors import HttpError

import warnings
warnings.filterwarnings('ignore')

# Replace with your own API key
DEVELOPER_KEY = st.secrets["API_KEY"]
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
# Create a client object to interact with the YouTube API
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

#video_id=extract_video_id(youtube_link)

def get_channel_id(video_id):
    response = youtube.videos().list(part='snippet', id=video_id).execute()
    channel_id = response['items'][0]['snippet']['channelId']
    return channel_id

#channel_id=get_channel_id(video_id)
    

def save_video_comments_to_csv(video_id):
    # Retrieve comments for the specified video using the comments().list() method
    comments = []
    results = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText'
    ).execute()
    
    # Extract the text content of each comment and add it to the comments list
    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            username = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comments.append([username,comment])
        if 'nextPageToken' in results:
            nextPage = results['nextPageToken']
            results = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                pageToken=nextPage
            ).execute()
        else:
            break
    
    # Save the comments to a CSV file with the video ID as the filename
    filename = video_id + '.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Username','Comment'])
        for comment in comments:
            writer.writerow([comment[0],comment[1]])
            
    return filename
            
def get_video_stats(video_id):
    try:
        response = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()

        return response['items'][0]['statistics']

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None
    
    
       
    
def get_channel_info(youtube, channel_id):
    try:
        response = youtube.channels().list(
            part='snippet,statistics,brandingSettings',
            id=channel_id
        ).execute()

        channel_title = response['items'][0]['snippet']['title']
        video_count = response['items'][0]['statistics']['videoCount']
        channel_logo_url = response['items'][0]['snippet']['thumbnails']['high']['url']
        channel_created_date = response['items'][0]['snippet']['publishedAt']
        subscriber_count = response['items'][0]['statistics']['subscriberCount']
        channel_description = response['items'][0]['snippet']['description']
        

        channel_info = {
            'channel_title': channel_title,
            'video_count': video_count,
            'channel_logo_url': channel_logo_url,
            'channel_created_date': channel_created_date,
            'subscriber_count': subscriber_count,
            'channel_description': channel_description
        }

        return channel_info

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

    

