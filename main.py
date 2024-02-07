# External libraries

import tweepy
from datetime import date
import datetime

# Local libraries

import config
import tw_functions
import sql_functions

# Connect to DB and API

conn = config.db_connect()
tw_client = config.tw_connect()

# Constants

num_days_total = 21
movie_date = '2022-02-25'
release_date = date.fromisoformat(movie_date)
start_date = datetime.datetime.combine(release_date - datetime.timedelta(days = 7), datetime.datetime.min.time())

# Get data

movies = sql_functions.get_movies(conn, release_date)

if movies is not None:

	for movie in movies:

		hashtag = movie[2]

		# query = "#" + hashtag + " place_country:US"
		query = "#" + hashtag

		print(query)

		tweets = tw_functions.tw_save_tweets(conn, query, movie, start_date, num_days_total)

		print("")

conn.close()

#rate_limit_status()