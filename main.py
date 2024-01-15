from dotenv import load_dotenv
import googleapiclient.errors
import googleapiclient.discovery
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
tokenizer = AutoTokenizer.from_pretrained(
    r'models\tokenizerbert')

model = AutoModelForSequenceClassification.from_pretrained(
    r'models\bertsenti')

load_dotenv()
api_key = os.getenv("API_KEY")


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


def commen(video_id, api_key):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=api_key)

    comments = get_comments(youtube, part="snippet",
                            videoId=video_id, textFormat="plainText")
    return comments


def get_video_comments(video_id):
    return commen(video_id, api_key)


def makevideoid(url):
    video_id = url.split("=")[1].split("&")[0]
    return video_id


def maxsent(result):
    return int(torch.argmax(result.logits))+1


def main():
    video = input("enter the url of the youtube video:")
    videoid = makevideoid(video)
    comments = get_video_comments(videoid)
    length = len(comments)
    num = 0
    for i in range(length):
        tokens = tokenizer.encode(comments[i], return_tensors='pt')
        result = model(tokens)
        num += maxsent(result)
    return (num/length)


if __name__ == "__main__":
    print(main())
