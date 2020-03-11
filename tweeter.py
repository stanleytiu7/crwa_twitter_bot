import tweepy
import time
import json
import tweepy
import pytz
from datetime import datetime
print('this is my twitter bot', flush=True)

with open("keys.json") as f:
    keys = json.load(f)

now = datetime.now()
current_time = now.strftime("%I:%M %p")

auth = tweepy.OAuthHandler(keys["CONSUMER_KEY"], keys["CONSUMER_SECRET"])
auth.set_access_token(keys["ACCESS_KEY"], keys["ACCESS_SECRET"])
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)

        mentioned = mention.full_text.lower()
        response_tweet = ' Last Update for '
        flag_status = ' Red '
        if '#location1' in mentioned:
            print('Found a query for #location1!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    response_tweet + '#location1 was '+ flag_status + current_time+ " EST", mention.id)
        elif "#location2" in mentioned:
            print('Found a query for #location2!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    response_tweet + ' #location2 was' + flag_status + 'Time:   '+current_time+ " EST", mention.id)
        


while True:
    reply_to_tweets()
    time.sleep(5)