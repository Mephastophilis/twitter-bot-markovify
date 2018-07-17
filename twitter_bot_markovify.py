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
import numpy as np
import os

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
    print("Text procudce completed")
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


def textproduce_b():
    checkpoint = 0
    while checkpoint == 0:
        fileoutput_a = open("time_line_a.txt", "w")
        fileoutput_b = open("time_line_b.txt", "w")

        for friend in user.friends():
            

            text_a = np.random.randint(2)
            if text_a == 1:
                print(friend.screen_name + ' used in corpus A.')
                for tweet in api.user_timeline(friend.screen_name, tweet_mode='extended', count = 30, include_rts = True):
                    tweettext = re.sub('https:\/\/.*', '', tweet.full_text.encode('ascii','ignore'))
                    tweettext = re.sub('&amp', '', tweettext)
                    tweettext = re.sub('\n',' ',tweettext)
                    fileoutput_a.write(tweettext + ' ')

            else:
                print(friend.screen_name + ' used in corpus B.')
                for tweet in api.user_timeline(friend.screen_name, tweet_mode='extended', count = 30, include_rts = True):
                    tweettext = re.sub('https:\/\/.*', '', tweet.full_text.encode('ascii','ignore'))
                    tweettext = re.sub('&amp', '', tweettext)
                    tweettext = re.sub('\n',' ',tweettext)
                    fileoutput_b.write(tweettext + ' ')     
        fileoutput_a.close
        fileoutput_b.close   
        
        if os.stat("time_line_a.txt").st_size == 0 or os.stat("time_line_b.txt").st_size == 0:
            open('time_line_a.txt', 'w').close()
            open('time_line_b.txt', 'w').close()
            print("One text file empty, redoing text distribution.")
        else:
            checkpoint = 1     

    



def randomtweet_b():

    file_a = open("time_line_a.txt", "r")
    file_b = open("time_line_b.txt", "r")
    corpus_a = file_a.read()
    corpus_b = file_b.read()
    file_a.close
    file_b.close

    model_a = markovify.Text(corpus_a)
    model_b = markovify.Text(corpus_b)
    model_combo = markovify.combine([ model_a, model_b ], [ 1, 1 ])
    newtweet = model_combo.make_short_sentence(random.randint(100,260))
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
    textproduce_b()
    for i in range(5):
        randomtweet()
        tweetcount=tweetcount+1
        print('tweet count = ' + str(tweetcount) + '. Model A used.')
        randomtweet_b()
        tweetcount=tweetcount+1
        print('tweet count = ' + str(tweetcount) + '. Model B used.')
        time.sleep(random.randint(40,100))
    time.sleep(300)