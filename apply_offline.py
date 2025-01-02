from flask import Flask, request, jsonify, render_template
from datetime import datetime
from textblob import TextBlob
import sqlite3
import json
import os
import joblib
from googlesearch import search  # Import Google Search miễn phí
from transformers import pipeline
import sqlite3
import json
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
emotion_log = {}

# ====== Tải dữ liệu phản hồi từ file JSON ======
try:
    with open("responses.json", "r", encoding="utf-8") as file:
        response_data = json.load(file)
except FileNotFoundError:
    response_data = {}

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
    if emotion != "neutral":
        if date not in emotion_log:
            emotion_log[date] = []
        if message not in emotion_log[date]:
            emotion_log[date].append(f"{emotion}: {message}")

# ====== HÀM LƯU CHAT VÀO DATABASE ======
def save_chat_to_db(user_message, bot_response):
    cursor.execute("INSERT INTO chat (user_message, bot_response) VALUES (?, ?)", (user_message, bot_response))
    conn.commit()

# ====== HÀM SCRAPING GOOGLE ======
def search_google_free(query):
    """
    Tìm kiếm Google và trả về kết quả liên quan.
    """
    results = []
    try:
        for url in search(query, num_results=5):  # Lấy 5 kết quả đầu tiên
            results.append(url)
    except Exception as e:
        results.append(f"Không thể tìm kiếm Google ngay lúc này. Lỗi: {str(e)}")
    return results

# ====== TẢI MÔ HÌNH AI ======
model = joblib.load("chatbot_model.pkl")

def generate_ai_response(message):
    """
    Tạo phản hồi dựa trên dữ liệu JSON hoặc tìm kiếm Google.
    """
    for keyword, responses in response_data.items():
        if keyword in message.lower():
            for response in responses:
                if isinstance(response, dict):  # Nếu phản hồi có cấu trúc nâng cao
                    bot_response = response["text"]
                    if response.get("search"):  # Nếu có tìm kiếm Google
                        search_results = search_google_free(response["search"])
                        bot_response += "\nDưới đây là một số thông tin tôi tìm được:\n"
                        for link in search_results[:3]:
                            bot_response += f"- {link}\n"
                    return bot_response
                else:
                    return response  # Phản hồi dạng chuỗi thông thường

    # Phản hồi mặc định nếu không có từ khóa phù hợp
    return "Tôi đang nghe bạn, hãy chia sẻ thêm nhé!"

# ====== TRANG CHÍNH ======
@app.route("/")
def home():
    return render_template("index.html", emotion_log=emotion_log)

# ====== API XỬ LÝ CHAT ======
@app.route("/chat", methods=["POST"])
def chat():
    """
    Xử lý tin nhắn từ người dùng, phân tích cảm xúc và trả lời.
    """
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Tin nhắn của bạn trống. Vui lòng nhập nội dung."}), 400

    date = datetime.now().strftime("%Y-%m-%d")
    sentiment = analyze_emotion_with_textblob(user_message)
    add_emotion_to_log(date, sentiment, user_message)

    bot_response = generate_ai_response(user_message)
    save_chat_to_db(user_message, bot_response)

    return jsonify({"response": bot_response})

# ====== API XEM LỊCH SỬ CHAT ======
@app.route("/get_chat_history", methods=["GET"])
def get_chat_history():
    """
    Trả về lịch sử chat từ database.
    """
    cursor.execute("SELECT user_message, bot_response, timestamp FROM chat")
    rows = cursor.fetchall()
    formatted_history = [{"user": row[0], "bot": row[1], "timestamp": row[2]} for row in rows]
    return jsonify({"chat_history": formatted_history})

# ====== API XEM NHẬT KÝ CẢM XÚC ======
@app.route("/log_emotion", methods=["GET"])
def log_emotion():
    """
    Trả về nhật ký cảm xúc theo ngày.
    """
    formatted_log = {
        date: {"entries": emotions, "count": len(emotions)}
        for date, emotions in emotion_log.items()
    }
    return jsonify({"emotions": formatted_log})

# ====== TỰ ĐỘNG CHẠY TIỀN XỬ LÝ, HUẤN LUYỆN ======
print("Bắt đầu tiền xử lý dữ liệu...")
os.system("python process_data.py")

print("Bắt đầu huấn luyện mô hình...")
os.system("python train_model.py")

print("Kiểm tra mô hình (tùy chọn)...")
os.system("python test_model.py")
# Kết nối database
conn = sqlite3.connect("chat_history.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    bot_response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# Phân tích cảm xúc
emotion_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Trả lời người dùng
def generate_response(message):
    # Phân tích cảm xúc
    emotion = emotion_analyzer(message)[0]['label']
    if emotion == "positive":
        return "Tôi rất vui khi nghe điều này! Hãy chia sẻ thêm nhé."
    elif emotion == "negative":
        return "Có vẻ bạn đang buồn, tôi luôn ở đây để lắng nghe bạn."
    else:
        return "Tôi ở đây để giúp bạn. Hãy nói rõ hơn để tôi hiểu nhé."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Tin nhắn của bạn trống. Vui lòng nhập nội dung."}), 400

    # Tạo phản hồi
    bot_response = generate_response(user_message)

    # Lưu vào database
    cursor.execute("INSERT INTO chat (user_message, bot_response) VALUES (?, ?)", (user_message, bot_response))
    conn.commit()

    return jsonify({"response": bot_response})
# ====== CHẠY ỨNG DỤNG ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



