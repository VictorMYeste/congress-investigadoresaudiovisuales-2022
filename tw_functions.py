# Search tweets from query

def tw_save_tweets(conn, query, movie, start_date, num_days):

	import tweepy
	import datetime
	import config
	import sql_functions
	import time

	tw_client = config.tw_connect()

	tweets = []

	end_date = start_date + datetime.timedelta(days = num_days)

	print(start_date)
	print(end_date)

	# Rate limit: 300 requests / 15 mins. 1 request / second
	# Total limit to not overuse all month limit: 300*500 = 150.000
	for response in tweepy.Paginator(tw_client.search_all_tweets, query = query, max_results = 500, limit = 150000, tweet_fields= ['created_at', 'public_metrics'], expansions = 'author_id', start_time = start_date, end_time = end_date):
		print("Request!")
		if response.data is not None:
			print("Tweets requested: %s" % len(response.data))
			for tweet in response.data:
				sql_functions.save_tweet(conn, movie, tweet)
		time.sleep(1)

def clean_tweet(tweet):

		import re

		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
		
		from textblob import TextBlob

		# create TextBlob object of passed tweet text
		analysis = TextBlob(clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 1
		elif analysis.sentiment.polarity == 0:
			return 0
		else:
			return -1

# Get users list from the includes object
#		users = {u["id"]: u for u in response.includes['users']}
#		
#		for tweet in response.data:
#			print(tweet.id)
#			if users[tweet.author_id]:
#				user = users[tweet.author_id]
#				print(user.profile_image_url)