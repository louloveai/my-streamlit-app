 from flask import Flask, request, jsonify, render_template
import json
import os

# Tạo ứng dụng Flask
app = Flask(__name__)

# Đường dẫn file dữ liệu training
DATA_FILE = "training_data.json"

# Load dữ liệu từ file JSON
def load_training_data(file_name=DATA_FILE):
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)

training_data = load_training_data()

# Hàm nhận diện cảm xúc
def detect_emotion(input_text):
    for entry in training_data:
        if entry["emotion"] in input_text.lower():
            return entry["emotion"], entry["response"]
    return "Không xác định", "Tôi chưa hiểu được cảm xúc
from flask import Flask, request, jsonify, render_template
import json
import sqlite3
import os
from datetime import datetime

# Tạo ứng dụng Flask
app = Flask(__name__)

# Đường dẫn file dữ liệu training
DATA_FILE = "training_data.json"

# Tên file SQLite
DB_FILE = "emotion_history.db"

# Kết nối SQLite
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emotion_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emotion TEXT,
            input_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Lưu lịch sử cảm xúc vào SQLite
def save_emotion_to_db(emotion, input_text):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO emotion_history (emotion, input_text) VALUES (?, ?)
    """, (emotion, input_text))
    conn.commit()
    conn.close()

# Load lịch sử cảm xúc từ SQLite
def load_emotion_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT emotion, input_text, timestamp FROM emotion_history ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Load dữ liệu từ file JSON
def load_training_data(file_name=DATA_FILE):
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)

training_data = load_training_data()

# Hàm nhận diện cảm xúc
def detect_emotion(input_text):
    for entry in training_data:
        if entry["emotion"] in input_text.lower():
            return entry["emotion"], entry["response"]
    return "Không xác định", "Tôi chưa hiểu được cảm xúc của bạn. 

