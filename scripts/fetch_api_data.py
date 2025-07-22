from pymongo import MongoClient
import certifi
import requests
import datetime

uri = "mongodb+srv://Aritra:Aritra98@cluster0.qvndesi.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["real_time_pipeline"]
collection = db["crypto_data"]

# Sample API
url = url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    data["timestamp"] = datetime.datetime.utcnow()
    result = collection.insert_one(data)
    print(f"Inserted ID: {result.inserted_id}")
else:
    print("Failed to fetch data:", response.status_code)
