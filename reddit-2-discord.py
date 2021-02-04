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
        new_posts = r.subreddit(sub).new(limit=config.limit)
        for post in new_posts:
            list = ["jpg", "gif", "png"]
            if post.url[-3:] in list:
                embed = {"color": random.randint(0, 0xffffff),
                         "image": {"url": post.url},
                         "fields": [{"name": "Title:", "value": post.title},
                                    {"name": "Author:", "value": "u/{}".format(str(post.author)),"inline": True},
                                    {"name": "Subreddit:", "value": "r/{}".format(str(post.subreddit)),"inline":True},
                                    {"name": "Upvotes:", "value": post.score, "inline":True},
                                    {"name": "Link to Post:",
                                     "value": "https://reddit.com/r/{}/comments/{}".format(str(post.subreddit),
                                                                                           str(post))}]}
            else:
                embed = {"color": random.randint(0, 0xffffff),
                         "fields": [{"name": "Title:", "value": post.title},
                                    {"name": "Author:", "value": "u/{}".format(str(post.author))},
                                    {"name": "Subreddit:", "value": "r/{}".format(str(post.subreddit))},
                                    {"name": "Link to Post:",
                                     "value": "https://reddit.com/r/{}/comments/{}".format(str(post.subreddit),
                                                                                           str(post))},
                                    {"name": "Upvotes:", "value": post.score}]}
            data = {"embeds": [embed]}
            response = requests.post(config.webhook_url, json=data)
            if response.status_code == 204:
                print("A new reddit post has arrived.")
            time.sleep(config.wait_time)


schedule.every(1).minutes.do(new_posts)
while True:
    schedule.run_pending()
    time.sleep(1)
