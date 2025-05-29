from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLL_NAME")]

@app.route("/data", methods=["GET"])
def get_data():
    data = list(collection.find({}))
    for item in data:
        item['_id'] = str(item['_id'])
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')


