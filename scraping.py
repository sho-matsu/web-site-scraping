# coding: UTF-8
import urllib2
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=''

cred = credentials.Certificate('')
default_app = firebase_admin.initialize_app(cred)

# アクセスするURL
url = ""

html = urllib2.urlopen(url)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html, "html.parser")

divs = soup.find_all("div", class_="h2bg")
months = []
for div in divs:
    value = div.find("h2").string
    if (value == ""):
        continue
    months.append(value)
#
# for m in months:
#     print m

db = firestore.Client()
collection = db.collection("garbage_collection")

days = []
tables = soup.find_all("table")
index = 0
for table in tables:
    month = months[index]
    index = index + 1
    values = table.find_all("td", class_="top")
    for value in values:
        if (str(value).find("日") < 0): continue
        if (len(value.contents) < 4): continue
        day = month + value.contents[0]
        description = value.contents[3]
        try:
            doc = collection.document(day)
            doc.set({
                "description": description
            })
        except:
            print day + ":" + description
            continue
        days.append([day, description])
