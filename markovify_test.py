#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Markovify test

Created on Tue Jun 19 16:10:34 2018

@author: faustus
"""

import tweepy
import re
import markovify



consumer_key = '8NldZNfZHaSOsiVzJlBHVfDpp'
consumer_secret = '3s8mleKXhUxhkhaYyAFMwa2CO3mXLQx7sXovrKaB5eDanHOCNb'
access_token = '1008861832197689344-KQg7ETt72SxpXBYEckdNWs4hs69dnM'
access_token_secret = 'Efgoyc0OD88Bra76DKEXPT5Sxq1HujhSmVX0TE4wZRBCH'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()

fileoutput = open("time_line.txt", "w") 
for friend in user.friends():
    print(friend.screen_name)
    for tweet in api.user_timeline(friend.screen_name, tweet_mode='extended', count = 10, include_rts = False):      
        tweettext = re.sub('https:\/\/.*', '', tweet.full_text.encode('ascii','ignore'))
        tweettext = re.sub('&amp', '', tweettext)
        tweettext = re.sub('\n',' ',tweettext)
        fileoutput.write(tweettext + '\n')
fileoutput.close    

file = open("time_line.txt", "r")
corpus = file.read()
file.close
text_model = markovify.Text(corpus)

for i in range(3):
    print(text_model.make_short_sentence(140))