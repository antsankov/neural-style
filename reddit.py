import praw
import random
import urllib
import os

from subprocess import call

reddit = praw.Reddit(client_id=os.getenv('client_id'),
                     client_secret=os.getenv('client_secret'),
                     user_agent=os.getenv('my ArtFactoryBot')

subreddit = reddit.subreddit('art')
top = []
for submission in subreddit.top('day'):
    top.append(submission)

content = top[random.randint(5,9)].url
print content
urllib.urlretrieve(content, 'content')


style = top[random.randint(5,9)].url
print style
urllib.urlretrieve(style, 'style')

# make seperate directory for everything

def neural_style(style, content):
    call([
        "th", "neural_styleneural_style.lua",
        "-gpu", "0",
        "-style_image", style, 
        "-content_image", content, 
        "-output_image", "output.png"],
        "-style_weight", "1000",
        "-image_size", "512",
        "-save_iter", "0")
        # "-original_colors", "1"
    ])
