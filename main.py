from twitter import *
from dotenv import load_dotenv
import os
import sqlite3
import pandas as pd

load_dotenv()
token = os.getenv("token")
token_secrets = os.getenv("token_secrets")
consumer_key = os.getenv("consumer_key")
consumer_secrets = os.getenv("consumer_secrets")

t = Twitter(auth=OAuth(token, token_secrets, consumer_key, consumer_secrets))

# Create db connection
db_path = './db/dummy-speed.db'  # your database path
cnx = sqlite3.connect(db_path)
df = pd.read_sql_query(
    "select round(ping, 3) as ping, round(download,3) as download, round(upload,3) as upload from speedtests order by created_at desc limit 1", cnx).to_string(index=None)

ping = pd.read_sql_query(
    "select round(ping, 2) as ping from speedtests order by created_at desc limit 1", cnx).to_string(index=None)
download = pd.read_sql_query(
    "select round(download,2) as download from speedtests order by created_at desc limit 1", cnx).to_string(index=None)
upload = pd.read_sql_query(
    "select round(upload,2) as upload from speedtests order by created_at desc limit 1", cnx).to_string(index=None)
url = pd.read_sql_query(
    "select url as [] from speedtests order by created_at desc limit 1", cnx).to_string(index=None)

# # Update a range of cells using the top left corner address
# next_tweet = "Todays ping report: \n" + \
#     ping + "\n " + download + "\n " + upload + "\n " + url
next_tweet = " Todays ping report: \n" + df + "\n " + url
print(next_tweet)

# post tweet through twitter API
t.statuses.update(status=next_tweet)
