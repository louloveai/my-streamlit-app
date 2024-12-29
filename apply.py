from flask import Flask, request, jsonify
import json
import os
import sqlite3

# Tạo ứng dụng Flask
app = Flask(__name__)

# Đường dẫn file dữ liệu training
DATA_FILE = "training_data.json"

# Tên file SQLite
DB_FILE = "emotion_history.db"

# Khởi tạo cơ sở dữ liệu SQLite
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
    if not os.path.exists(file_name):
        return []
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)

training_data = load_training_data()

# Hàm nhận diện cảm xúc
def detect_emotion(input_text):
    for entry in training_data:
        for response in entry["responses"]:
            if response["input"] in input_text.lower():
                return entry["emotion"], response["response"]
    return "Không xác định", "Tôi chưa hiểu được cảm xúc của bạn."

# API phân tích cảm xúc
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    user_input = data.get("text", "").strip()
    if not user_input:
        return jsonify({"error": "Vui lòng cung cấp văn bản để phân tích."}), 400

    emotion, response = detect_emotion(user_input)
    save_emotion_to_db(emotion, user_input)
    return jsonify({"emotion": emotion, "response": response})

# API lấy lịch sử cảm xúc
@app.route("/history", methods=["GET"])
def history():
    history_data = load_emotion_history()
    return jsonify(history_data)

# Khởi động ứng dụng
if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))  # Lấy cổng từ biến môi trường hoặc mặc định là 5000
    app.run(host="0.0.0.0", port=port, debug=True)

# Định nghĩa route cho URL gốc "/"
@app.route("/")
def home():
    return "Ứng dụng Flask của bạn đã chạy thành công! Hãy truy cập các endpoint khác để kiểm tra chức năng."

