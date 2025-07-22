import os
from pymongo import MongoClient
import certifi
import requests
import datetime
import socket

# Force IPv4 to avoid DNS issues on GitHub runners
orig_getaddrinfo = socket.getaddrinfo
def getaddrinfo_ipv4(*args, **kwargs):
    return [ai for ai in orig_getaddrinfo(*args, **kwargs) if ai[0] == socket.AF_INET]
socket.getaddrinfo = getaddrinfo_ipv4

uri = os.environ["MONGO_URI"]
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["real_time_pipeline"]
collection = db["crypto_data"]

url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    data["timestamp"] = datetime.datetime.utcnow()
    result = collection.insert_one(data)
    print(f"Inserted ID: {result.inserted_id}")
else:
    print("Failed to fetch data:", response.status_code)
