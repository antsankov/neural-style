import praw
import random
import urllib
import os, datetime
import tinys3
import argparse
from subprocess import call

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--content') 
    parser.add_argument('--style') 
    args = parser.parse_args()

    dir_path = datetime.datetime.now().strftime('af/%Y-%m-%d_%H-%M-%S')
    content_path = dir_path + '/content'
    style_path = dir_path + '/style'
    output_path = dir_path + '/output' + time + '.png' 

    dir = os.path.join(os.getcwd(), dir_path)
    os.makedirs(dir)

    urllib.urlretrieve(args.style, style_path)
    urllib.urlretrieve(args.content, content_path)
    
    # gather_from_subreddit('artporn', content_path, style_path)
    neural_style(style_path, content_path, output_path, "0")
    # neural_style(style_path, content_path, output_path_preserve, "1")

    upload_to_s3(output_path)


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

def upload_to_s3(file_path):
    conn = tinys3.Connection(
        os.getenv('S3_ACCESS_KEY'),os.getenv('S3_SECRET_KEY'),tls=True
    )
    f = open(file_path,'rb')
    conn.upload(file_path,f,'art-factory')
    

def neural_style(style, content, output, original_colors):
    call([
        "th", "neural_style.lua",
        "-gpu", "0",
        "-style_image", style, 
        "-content_image", content, 
        "-output_image", output,
        "-style_weight", "1000",
        "-image_size", "1024",
        "-save_iter", "0",
        "-original_colors", original_colors
    ])

if __name__ == "__main__":
    main()
