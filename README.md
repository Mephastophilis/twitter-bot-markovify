# twitter-bot-markovify

Python twitter bot using tweepy and markovify. The bot draws the most recent tweets from its followers and uses Markov chains to compose original tweets.

# Setup
Enter the consumer key, consumer secret, access token, and access token secret into the credentials.txt. Each on a seperate line and in that order. Next choose a selection of people to follow, by entering them into the follow_list.txt. Enter the twitter usernames with the @ each on a seperate line in the text file. If your bot's twitter account is already following the people you are interested in, then just leave that document blank. 

# Running
Once the you have entered your credentials and follow list, run twitter_bot_markovify.py and enjoy. The bot tweets a pair of tweets each about every minute. The first tweet in the pair comes from a simple Markov chain model, while the second tweet is a more complex model that is a combination of your different followers.
