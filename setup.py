#!/usr/bin/python3

import requests
import re
import sqlite3
import os
from collections import defaultdict
from bs4 import BeautifulSoup

base_url = 'https://www.ece.tuc.gr'
ids = [4519, 4523, 4531, 6756]

dir = os.path.expanduser('~/.config/tucfetch')
db = dir + '/avatars.sqlite'

# Function to add key/value pairs for a user
def add_user_attributes(user_id, attributes):
    for key, value in attributes.items():
        key = key[:-1]
        value = value.replace("<at>", "@")
        cursor.execute('''
        INSERT INTO UserAttributes (user_id, key, value)
        VALUES (?, ?, ?)
        ''', (user_id, key, value))
    conn.commit()

# Base directory
print('[*] Creating tucfetch directory..')
os.makedirs(dir, exist_ok=True)

# Remove the db if it exists
if os.path.exists(db):
    os.remove(db)

# Connect to the SQLite database (it will create a new database file if it doesn't exist)
print('[*] Setting up db..')
conn = sqlite3.connect(db)

# Create a cursor object
cursor = conn.cursor()

# Create avatar table
cursor.execute('''
CREATE TABLE IF NOT EXISTS UserAttributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL
)
''')

# Get profile links
print('[*] Fetching profile links..')
profiles = []
for id in ids:
    r = requests.get(f'https://www.ece.tuc.gr/en/index.php?id={id}')
    page_html = r.text.splitlines()
    for line in page_html:
        if re.search("tuclabspersonnel_list", line):
            profile_link = re.findall(r'href=["\'](.*?)["\']', line)
            profile_link = profile_link[0].replace("&amp;", "&")
            profiles.append(base_url + profile_link)

profiles = sorted(set(profiles))

# Get profile data
print('[*] Getting avatars and user data..')
users_data = defaultdict(dict)
user_id = 0
for profile in profiles:
    r = requests.get(profile)

    # Profile picture
    pfp_link = str(re.findall(r'src=[\'\'](.*?)[\'\']', r.text)[0])
    if "default.png" in pfp_link: # Skip if there is no pfp
        continue

    # Get name
    name = re.findall(r'"name":\s*"([^"]+)"', r.text)[0]
    # Download pfp
    img_data = requests.get(pfp_link).content
    filename = name.lower().replace(" ", "_") + ".jpg"
    avatars_dir = dir + '/avatars/'
    os.makedirs(avatars_dir, exist_ok=True)
    with open(avatars_dir + filename, 'wb') as handler:
        handler.write(img_data)
    users_data[user_id]["Profile Picture:"] = avatars_dir + filename

    # Get data table
    page_html = r.text.splitlines()
    for line in page_html:
        if re.search("datatable", line):
            soup = BeautifulSoup(line, "html.parser")
            tr = soup.find_all('tr')
            for td_class in tr:
                try:
                    td = td_class.find('td')
                    users_data[user_id][td.text] = td.find_next().text
                except:
                    continue
            break

    user_id += 1

users_data = dict(users_data)

# Add attributes for each user
print('[*] Updating db..')
for user_id, attributes in users_data.items():
    add_user_attributes(user_id, attributes)

# Close connection
conn.close()

print('[+] Finished installation')
