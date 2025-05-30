from flask import Flask, jsonify, Response
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from flask_cors import CORS
import os
import json
import time
from dotenv import load_dotenv, dotenv_values

load_dotenv()

print(dotenv_values())

app = Flask(__name__)
CORS(app)

# Read environment variables (works both locally and in Docker Compose)
mongo_url = os.getenv("MONGO_URI", "mongodb://mongo:27017")
db_name = os.getenv("DB_NAME", "DesignersDB")
coll_name = os.getenv("COLL_NAME", "Designers")

print("Connecting to MongoDB at:", mongo_url)

# Setup MongoDB client
client = MongoClient(mongo_url)

# Retry loop to wait for MongoDB readiness
max_retries = 2
for attempt in range(max_retries):
    try:
        client.admin.command('ping')  # ping MongoDB
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
    print("data: ",data)
    for item in data:
        item['_id'] = str(item['_id'])  

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
