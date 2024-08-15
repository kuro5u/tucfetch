#!/usr/bin/python3

import sqlite3
import random
import os

dir = os.path.expanduser('~/.config/tucfetch')
config = dir + '/config.conf'

# Connect to the SQLite database (it will create a new database file if it doesn't exist)
conn = sqlite3.connect(dir + '/avatars.sqlite')

# Create a cursor object
cursor = conn.cursor()

# Function to get a random user_id
def get_random_user_id():
    cursor.execute('SELECT DISTINCT user_id FROM UserAttributes')
    user_ids = cursor.fetchall()
    if user_ids:
        return random.choice(user_ids)[0]  # Return a random user_id
    return None

# Function to get attributes for a given user_id
def get_user_attributes(user_id):
    cursor.execute('SELECT key, value FROM UserAttributes WHERE user_id = ?', (user_id,))
    return cursor.fetchall()

# Get a random user_id
random_user_id = get_random_user_id()

# Get and print the attributes for the random user_id
attributes = get_user_attributes(random_user_id)

# Close the connection
conn.close()

# Set data as env variables
for i in range(1, len(attributes)):
    key = attributes[i][0]
    value = attributes[i][1]
    os.environ[f"KEY{i}"] = key
    os.environ[f"VALUE{i}"] = value

# TUCfetch
pfp_path = attributes[0][1]
os.system(f"neofetch --config {config} --chafa {pfp_path} --size 410px")
