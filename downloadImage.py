import os
import requests
from pymongo import MongoClient
import urllib.request

# Mongo db connection
HOST = 'cluster0.n76ap.mongodb.net'
USER = 'admin'
PASSWORD = ''
DATABASE_NAME = 'myFirstDatabase'
COLLECTION_NAME = ['maskURL','nomaskURL']
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

for c_name in COLLECTION_NAME:
    collection = db[c_name]
    # Path for images to be saved
    img_dir_path = str(os.getcwd()) + f'/images/{c_name}'
    # Create directory if doesn't exist
    if not os.path.exists(img_dir_path):
        os.makedirs(img_dir_path)

    # Make header like actual User not a program
    opener = urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)
    
    # Download images using url in mongoDB
    idx = 0
    for url_info in collection.find():
        file_name = f"{idx:150}.jpg"
        try:
            urllib.request.urlretrieve(url_info['URL'], os.path.join(img_dir_path, file_name))
            idx += 1
        except Exception as e:
            print(f"ERROR DOWNLOADING {url_info['URL']} - {e}")