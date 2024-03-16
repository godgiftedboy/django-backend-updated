import googleapiclient.discovery
import pandas as pd

def scrap_comments(videoID,apiKey,numberofcomments):

    dev = apiKey
    # "AIzaSyDBD2XxnPKGsYsoZ6RS0Wu0f2UKS_fmxu0"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = dev

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    numberofcomments = int(numberofcomments)
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=videoID,
        maxResults=numberofcomments
    )

    comments = []
    # list to store comments

    # Execute the request.
    response = request.execute()

    # Get the comments from the response.
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
    #     public = item['snippet']['isPublic']
        comments.append([
            # comment['authorDisplayName'],
            # comment['publishedAt'],
            # comment['likeCount'],
            comment['textOriginal'],
    #         public
        ])
    
    return comments

