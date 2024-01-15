import streamlit as st
from dotenv import load_dotenv
import googleapiclient.errors
import googleapiclient.discovery
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


tokenizer = AutoTokenizer.from_pretrained(
    'nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained(
    'nlptown/bert-base-multilingual-uncased-sentiment')

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


def get_video_comments(video_id, api_key):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=api_key)

    comments = get_comments(youtube, part="snippet",
                            videoId=video_id, textFormat="plainText")
    return comments


def makevideoid(url):
    video_id = url.split("=")[1].split("&")[0]
    return video_id


st.title("YouTube Comment Sentiment Analysis")

# User input for video URL
video_url = st.text_input("Enter YouTube Video URL")


# Create a radio button


# Content to be displayed based on the radio button state


if video_url:

    videoid = makevideoid(video_url)
    comments = get_video_comments(videoid, api_key)

    # Display comments and sentiment analysis
    num = 0
    with st.expander("Comment with sentiment analysis"):
        for i, comment in enumerate(comments, 1):
            tokens = tokenizer.encode(
                comment, return_tensors='pt', max_length=512)
            result = model(tokens)
            sentiment = int(torch.argmax(result.logits)) + 1
            num += sentiment

            st.write(f"Comment {i}: {comment} (Sentiment: {sentiment})")
    st.title(num/len(comments))
