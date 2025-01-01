from flask import Flask, request, jsonify, render_template
from datetime import datetime
from textblob import TextBlob
import json

app = Flask(__name__)

# Lưu trữ lịch sử chat và nhật ký cảm xúc
chat_history = []
emotion_log = {}  # Lưu cảm xúc theo ngày

# Load phản hồi từ file JSON
with open("responses.json", "r", encoding="utf-8") as file:
    response_data = json.load(file)

# Hàm phân tích cảm xúc cơ bản với TextBlob
def analyze_emotion_with_textblob(message):
    analysis = TextBlob(message)
    polarity = analysis.sentiment.polarity  # Giá trị từ -1 (tiêu cực) đến 1 (tích cực)

    if polarity < -0.3:
        return "negative"
    elif polarity > 0.3:
        return "positive"
    else:
        return "neutral"

# Hàm lưu cảm xúc vào nhật ký theo ngày
def add_emotion_to_log(message):
    date = datetime.now().strftime("%Y-%m-%d")  # Ngày hiện tại
    if date not in emotion_log:
        emotion_log[date] = []
    emotion_log[date].append(message)

# Hàm tạo phản hồi AI thông minh
def generate_ai_response(message):
    sentiment = analyze_emotion_with_textblob(message)

    # Dựa trên sentiment
    if sentiment == "negative":
        return "Tôi rất tiếc khi nghe điều này. Bạn muốn chia sẻ thêm không?"
    elif sentiment == "positive":
        return "Thật tuyệt vời! Tôi rất vui khi nghe điều này từ bạn."
    
    # Tìm phản hồi dựa trên từ khóa
    for keyword, responses in response_data.items():
        if keyword in message.lower():
            return responses[0]  # Trả lời câu đầu tiên từ responses.json

    # Default response
    return "Tôi đang lắng nghe bạn, hãy kể thêm nhé!"

# Trang chính
@app.route("/")
def home():
    return render_template("index.html", chat_history=chat_history, emotion_log=emotion_log)

# Xử lý tin nhắn người dùng
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()  # Đảm bảo dữ liệu POST là JSON
    if not data or "message" not in data:
        return jsonify({"error": "Invalid data"}), 400

    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"response": "Tin nhắn của bạn trống. Vui lòng nhập nội dung."}), 400

    # Phân tích và lưu cảm xúc nếu cần
    if analyze_emotion_with_textblob(user_message) != "neutral":
        add_emotion_to_log(user_message)

    # Tạo phản hồi AI
    bot_response = generate_ai_response(user_message)

    # Lưu vào lịch sử chat
    chat_history.append({"user": user_message, "bot": bot_response})

    # Giới hạn lịch sử chat để tránh tràn bộ nhớ
    if len(chat_history) > 100:
        chat_history.pop(0)

    return jsonify({"response": bot_response, "chat_history": chat_history})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




