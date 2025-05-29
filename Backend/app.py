from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load environment variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

@app.route("/data", methods=["GET"])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM designers;")  # replace 'designers' with your table name
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

# from flask import Flask, jsonify
# from pymongo import MongoClient
# from dotenv import load_dotenv
# from flask_cors import CORS
# import os

# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# MONGO_URI = os.getenv("MONGO_URI")
# client = MongoClient(MONGO_URI)
# db = client[os.getenv("DATABASE_NAME")]
# collection = db[os.getenv("COLLECTION_NAME")]

# @app.route("/data", methods=["GET"])
# def get_data():
#     data = list(collection.find({}))
#     # Convert ObjectId to string
#     for item in data:
#         item['_id'] = str(item['_id'])
#     return jsonify(data)

# if __name__ == "__main__":
#     app.run(debug=True)
