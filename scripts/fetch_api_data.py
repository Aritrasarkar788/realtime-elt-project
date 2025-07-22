import requests
import pymongo
import os
from datetime import datetime

# Reads MongoDB connection URI from environment variable
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client["realtime_db"]
collection = db["api_data"]

# Fetch data from public API (example: exchange_rate)
response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")

if response.status_code == 200:
    data = response.json()
    data["_fetched_at"] = datetime.utcnow()
    collection.insert_one(data)
    print("Data inserted to MongoDB.")
else:
    print(f"❌ API failed: {response.status_code}")
