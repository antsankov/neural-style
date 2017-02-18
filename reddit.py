import praw
import random
import urllib
import os, datetime

from subprocess import call


def main():

    dir_path = datetime.datetime.now().strftime('af_%Y-%m-%d_%H-%M-%S')
    content_path = dir_path + '/content'
    style_path = dir_path + '/style'
    output_path = dir_path + '/output.png'

    dir = os.path.join(os.getcwd(), dir_path)
    os.makedirs(dir)

    gather_from_subreddit('art', content_path, style_path)
    neural_style(style_path, content_path, output_path)


def gather_from_subreddit(sub, content_path, style_path):
    reddit = praw.Reddit(client_id=os.getenv('client_id'),
                         client_secret=os.getenv('client_secret'),
                         user_agent='my ArtFactoryBot')


    subreddit = reddit.subreddit(sub)
    top = []
    for submission in subreddit.top('day'):
        top.append(submission)

    content = top[random.randint(0,4)].url 
    urllib.urlretrieve(content, content_path)


    style = top[random.randint(5,9)].url 
    urllib.urlretrieve(style, style_path)

def neural_style(style, content, output):
    call([
        "th", "neural_styleneural_style.lua",
        "-gpu", "0",
        "-style_image", style, 
        "-content_image", content, 
        "-output_image", output,
        "-style_weight", "1000",
        "-image_size", "512",
        "-save_iter", "0"
        # "-original_colors", "1"
    ])

if __name__ == "__main__":
    main()
