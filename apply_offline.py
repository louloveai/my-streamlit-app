from flask import Flask, request, jsonify, render_template
from datetime import datetime
from textblob import TextBlob
import sqlite3
import json
import os

app = Flask(__name__)

# ====== CẤU HÌNH DATABASE ======
# Kết nối SQLite
conn = sqlite3.connect("chat_history.db", check_same_thread=False)
cursor = conn.cursor()

# Tạo bảng lịch sử chat
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    bot_response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# ====== Lưu trữ cảm xúc ======
emotion_log = {}  # Lưu cảm xúc theo ngày

# ====== Tải dữ liệu phản hồi từ file JSON ======
try:
    with open("responses.json", "r", encoding="utf-8") as file:
        response_data = json.load(file)
except FileNotFoundError:
    response_data = {}  # Dữ liệu phản hồi mặc định

# ====== HÀM PHÂN TÍCH CẢM XÚC ======
def analyze_emotion_with_textblob(message):
    analysis = TextBlob(message)
    polarity = analysis.sentiment.polarity
    if polarity < -0.3:
        return "negative"
    elif polarity > 0.3:
        return "positive"
    return "neutral"

# ====== HÀM LƯU CẢM XÚC ======
def add_emotion_to_log(date, emotion, message):
    if emotion != "neutral":  # Bỏ qua cảm xúc trung tính
        if date not in emotion_log:
            emotion_log[date] = []
        if message not in emotion_log[date]:
            emotion_log[date].append(f"{emotion}: {message}")

# ====== HÀM LƯU CHAT VÀO DATABASE ======
def save_chat_to_db(user_message, bot_response):
    cursor.execute("INSERT INTO chat (user_message, bot_response) VALUES (?, ?)", (user_message, bot_response))
    conn.commit()

# ====== HÀM TẠO PHẢN HỒI AI ======
def generate_ai_response(message):
    for keyword, responses in response_data.items():
        if keyword in message.lower():
            return responses[0]  # Trả về phản hồi đầu tiên từ responses.json
    return ("Chủ đề này thú vị đấy, nhưng tôi không rõ lắm. "
            "Bạn có thể tìm thêm thông tin trên Google hoặc chia sẻ thêm để tôi hiểu rõ hơn.")

# ====== TRANG CHÍNH ======
@app.route("/")
def home():
    return render_template("index.html", emotion_log=emotion_log)

# ====== API XỬ LÝ CHAT ======
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    # Kiểm tra tin nhắn rỗng
    if not user_message:
        return jsonify({"response": "Tin nhắn của bạn trống. Vui lòng nhập nội dung."}), 400

    # Phân tích cảm xúc
    date = datetime.now().strftime("%Y-%m-%d")
    sentiment = analyze_emotion_with_textblob(user_message)
    add_emotion_to_log(date, sentiment, user_message)

    # Tạo phản hồi từ AI
    bot_response = generate_ai_response(user_message)

    # Lưu vào database
    save_chat_to_db(user_message, bot_response)

    return jsonify({"response": bot_response})

# ====== API XEM LỊCH SỬ CHAT ======
@app.route("/get_chat_history", methods=["GET"])
def get_chat_history():
    cursor.execute("SELECT user_message, bot_response, timestamp FROM chat")
    rows = cursor.fetchall()
    formatted_history = [{"user": row[0], "bot": row[1], "timestamp": row[2]} for row in rows]
    return jsonify({"chat_history": formatted_history})

# ====== API XEM NHẬT KÝ CẢM XÚC ======
@app.route("/log_emotion", methods=["GET"])
def log_emotion():
    formatted_log = {
        date: {"entries": emotions, "count": len(emotions)}
        for date, emotions in emotion_log.items()
    }
    return jsonify({"emotions": formatted_log})
import joblib

# Tải mô hình đã huấn luyện
model = joblib.load("chatbot_model.pkl")

# Cập nhật hàm generate_ai_response
def generate_ai_response(message):
    """
    Dự đoán phản hồi dựa trên mô hình đã huấn luyện.
    """
    vectorized_message = vectorizer.transform([message])  # Vector hóa tin nhắn
    predicted_response = model.predict(vectorized_message)[0]
    return predicted_response

# ====== CHẠY ỨNG DỤNG ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



