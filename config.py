# Connect to SQLite database

def db_connect():

	import sqlite3
	from sqlite3 import Error

	db_file = r"c_invaud.db"

	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)

	return conn

# Connect to Twitter API

def tw_connect():

	import tweepy

	bearer_token = "*"

	tw_client = tweepy.Client(bearer_token = bearer_token, wait_on_rate_limit = True)
	
	return tw_client