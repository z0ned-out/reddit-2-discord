import praw
import time
import os
import requests
import json
import random
import config
import schedule
from time import sleep


def new_posts():
    r = praw.Reddit(username=config.username, password=config.password, client_id=config.client_id,
                    client_secret=config.client_secret, user_agent=config.user_agent)
    for sub in config.subreddits:
        new_posts = r.subreddit(sub)
        for post in new_posts.stream.submissions(skip_existing=True):
            list = ["jpg", "gif", "png"]
            if post.url[-3:] in list:
                embed = {"color": random.randint(0, 0xffffff),
                         "image": {"url": post.url},
                         "fields": [{"name": "Title:", "value": post.title},
                                    {"name": "Author:", "value": "u/{}".format(str(post.author)), "inline": True},
                                    {"name": "Subreddit:", "value": "r/{}".format(str(post.subreddit)),
                                     "inline": True},
                                    {"name": "Link to Post:",
                                     "value": "https://reddit.com/r/{}/comments/{}".format(str(post.subreddit),
                                                                                           str(post))},
                                    {"name": "Timestamp:",
                                     "value": time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(post.created_utc)),
                                     "inline": True}]}
            else:
                embed = {"color": random.randint(0, 0xffffff),
                         "fields": [{"name": "Title:", "value": post.title},
                                    {"name": "Author:", "value": "u/{}".format(str(post.author))},
                                    {"name": "Subreddit:", "value": "r/{}".format(str(post.subreddit))},
                                    {"name": "Link to Post:",
                                     "value": "https://reddit.com/r/{}/comments/{}".format(str(post.subreddit),
                                                                                           str(post))},
                                    {"name": "Timestamp:",
                                     "value": time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(post.created_utc)),
                                     "inline": True}]}
            data = {"embeds": [embed]}
            response = requests.post(config.webhook_url, json=data)
            if response.status_code == 204:
                print("A new astrophotography reddit post has arrived.")
                print(datetime.datetime.fromtimestamp(post.created_utc))
while True:
    new_posts()
    time.sleep(1)
