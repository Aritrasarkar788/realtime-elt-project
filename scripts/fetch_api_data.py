import requests
from pymongo import MongoClient
import certifi

# MongoDB connection
uri = "mongodb+srv://Aritra:Aritra98@cluster0.qvndesi.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["weather_data"]
collection = db["open_meteo"]

# API endpoint
url = "https://api.open-meteo.com/v1/forecast?latitude=22.57&longitude=88.36&hourly=temperature_2m"

# Fetch and insert data
try:
    response = requests.get(url)
    data = response.json()
    collection.insert_one(data)
    print("Data inserted successfully")
except Exception as e:
    print("Error fetching or inserting data:", e)
