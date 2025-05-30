from flask import Flask, jsonify, Response
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from flask_cors import CORS
import os
import json
import time
from dotenv import load_dotenv, dotenv_values
import threading
import requests

load_dotenv()

print(dotenv_values())

app = Flask(__name__)
CORS(app)

mongo_url = os.getenv("MONGO_URI", "mongodb://mongo:27017")
db_name = os.getenv("DB_NAME", "DesignersDB")
coll_name = os.getenv("COLL_NAME", "Designers")

print("Connecting to MongoDB at:", mongo_url)

client = MongoClient(mongo_url)

max_retries = 2
for attempt in range(max_retries):
    try:
        client.admin.command('ping') 
        print("MongoDB connection established.")
        break
    except ServerSelectionTimeoutError:
        print(f"MongoDB not ready, retrying ({attempt + 1}/{max_retries})...")
        time.sleep(2)
else:
    print("Could not connect to MongoDB after retries, exiting.")
    exit(1)

db = client[db_name]
collection = db[coll_name]

@app.route("/", methods=["GET"])
def greet():
    print("hiii", flush=True)
    return jsonify("Hello Welcome..! hi")

@app.route("/data", methods=["GET"])
def get_data():
    data = list(collection.find({}))
    # print("data: ", data)
    for item in data:
        item['_id'] = str(item['_id'])  
    return jsonify(data)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"}), 200

# Background thread to self-ping every 30 seconds
def ping_self():
    url = os.getenv("SELF_URL", "http://localhost:5000/ping")  # or your deployed URL
    while True:
        try:
            print("Website Reloaded....", flush=True)
            requests.get(url)
        except Exception as e:
            print("Ping failed:", e, flush=True)
        time.sleep(30)

if __name__ == '__main__':
    threading.Thread(target=ping_self, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
