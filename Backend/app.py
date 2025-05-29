from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
CORS(app)


mongo_url = os.environ.get("MONGO_URI")

client = MongoClient("mongodb://mongo:27017/")

if mongo_url:
    client = MongoClient(mongo_url)

db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLL_NAME")]


@app.route("/", methods=["GET"])
def greet():
    return jsonify("Hello Welcome..!")

@app.route("/data", methods=["GET"])
def get_data():
    data = list(collection.find({}))
    for item in data:
        item['_id'] = str(item['_id'])
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')


