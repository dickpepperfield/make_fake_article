import feedparser
import random

def loadTitle(get_args):
    feed = feedparser.parse(get_args.feed)
    with open('tmp/feeds', 'w') as f:
        for item in feed.entries:
            print(item[ "title" ], file=f) 

    Title = random.choice(list(open('tmp/feeds')))
    return Title
