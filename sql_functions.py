# Get movies from timepoint of next week
		
def get_movies(conn, release_date):

	import datetime
	import sqlite3
	
	cursor = conn.cursor()

	query = "SELECT * FROM movies WHERE release_date = '%s'"

	try:
		cursor.execute(query % (release_date))
	except sqlite3.IntegrityError as e:
		print("Error occurred: ", e)

	rows = cursor.fetchall()

	#movies = []
	#for movie in rows:
	#	movies.append(movie)

	return rows

# Change movie timepoints



# Save tweet in Database

def save_tweet(conn, movie, tweet):
	
	import tw_functions
	import sqlite3
	from datetime import date
	import datetime
	import pytz

	cursor = conn.cursor()

	movie_id = movie[0]
	movie_release_date = movie[3]

	release_date = date.fromisoformat(movie_release_date)
	release_date = datetime.datetime.combine(release_date, datetime.datetime.min.time())
	week_after_release_date = datetime.datetime.combine(release_date + datetime.timedelta(days = 7), datetime.datetime.min.time())

	utc=pytz.UTC
	release_date = utc.localize(release_date)
	week_after_release_date = utc.localize(week_after_release_date)

	timepoint = 2

	if tweet.created_at < release_date:
		timepoint = 1

	elif tweet.created_at > week_after_release_date:
		timepoint = 3

	tweet_data = (tweet.id, movie_id, timepoint, tweet.author_id, tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'), tweet.public_metrics['quote_count'], tweet.public_metrics['reply_count'], tweet.public_metrics['retweet_count'], tweet.public_metrics['like_count'], tw_functions.get_tweet_sentiment(tweet.text))

	query = '''
		INSERT INTO tweets(status_id, movie_id, timepoint, author_id, created_at, quote_count, 	reply_count, retweet_count, like_count, sentiment)
		VALUES(?,?,?,?,?,?,?,?,?,?)
	'''
	
	try:
		cursor.execute(query, tweet_data)
		conn.commit()
	except sqlite3.Error as e:
		print("Error occurred: ", e)