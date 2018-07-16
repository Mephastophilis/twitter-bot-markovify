#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Tweepy practice
"""

import tweepy
import nltk
import re
import random
import time
import markovify

credentials=[]

file = open("credentials.txt", "r")
for line in file:
    credentials.append(line.rstrip())
file.close

auth = tweepy.OAuthHandler(credentials[0], credentials[1])
auth.set_access_token(credentials[2], credentials[3])
api = tweepy.API(auth)

user = api.me()
print (user.name)
print(user.location)

file = open("follow_list.txt", "r")
for line in file:
    api.create_friendship(line.rstrip())
    print line.rstrip() + "followed"
file.close

def textproduce():
    fileoutput = open("time_line.txt", "w")
    for friend in user.friends():
        print(friend.screen_name)
        for tweet in api.user_timeline(friend.screen_name, tweet_mode='extended', count = 10, include_rts = False):
            tweettext = re.sub('https:\/\/.*', '', tweet.full_text.encode('ascii','ignore'))
            tweettext = re.sub('&amp', '', tweettext)
            tweettext = re.sub('\n',' ',tweettext)
            fileoutput.write(tweettext + ' ')
    fileoutput.close

def randomtweet():
    file = open("time_line.txt", "r")
    corpus = file.read()
    file.close
    text_model = markovify.Text(corpus)
    newtweet = text_model.make_short_sentence(random.randint(100,260))
    print(newtweet)
    for status in tweepy.Cursor(api.user_timeline).items():
        if newtweet == status.text:
            api.destroy_status(status.id)
            print('duplicate tweet destroyed')
        else:
            pass
    api.update_status(newtweet)

tweetcount=0
while True:
    textproduce()
    for i in range(5):
        randomtweet()
        tweetcount=tweetcount+1
        print('tweet count = ' + str(tweetcount))
        time.sleep(random.randint(40,300))
    time.sleep(300)
