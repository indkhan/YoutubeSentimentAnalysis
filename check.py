import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
print(api_key)


def get_comments(youtube, **kwargs):
    comments = []
    results = youtube.commentThreads().list(**kwargs).execute()

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        # check if there are more comments
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = youtube.commentThreads().list(**kwargs).execute()
        else:
            break

    return comments


def comm(video_id, api_key):
    # Disable OAuthlib's HTTPs verification when running locally.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=api_key)

    comments = get_comments(youtube, part="snippet",
                            videoId=video_id, textFormat="plainText")
    return comments


def get_video_comments(video_id):
    return comm(video_id, api_key)


def videoid(url):
    video_id = url.split("=")[1].split("&")[0]
    return video_id


video_id = videoid(
    "https://youtu.be/OlPO8f-AAJk?si=ebQ8SWDaGRIj2F-b")
print(video_id)


comm = get_video_comments(video_id)
print(comm)