from flask import Flask, request, jsonify, render_template
from datetime import datetime
from textblob import TextBlob
import json

app = Flask(__name__)

# ====== Lưu trữ lịch sử chat và nhật ký cảm xúc ======
chat_history = []  # Lịch sử chat giữa người dùng và AI
emotion_log = {}  # Lưu cảm xúc theo ngày

# ====== Tải dữ liệu phản hồi từ file JSON ======
with open("responses.json", "r", encoding="utf-8") as file:
    response_data = json.load(file)

# ====== Hàm phân tích cảm xúc cơ bản ======
def analyze_emotion_with_textblob(message):
    """
    Phân tích cảm xúc cơ bản của tin nhắn dựa trên TextBlob
    """
    analysis = TextBlob(message)
    polarity = analysis.sentiment.polarity
    if polarity < -0.3:
        return "negative"
    elif polarity > 0.3:
        return "positive"
    return "neutral"

# ====== Hàm lưu cảm xúc vào nhật ký ======
def add_emotion_to_log(date, message):
    """
    Lưu cảm xúc vào nhật ký theo ngày, tránh trùng lặp nội dung
    """
    if date not in emotion_log:
        emotion_log[date] = []
    if message not in emotion_log[date]:
        emotion_log[date].append(message)

# ====== Hàm tạo phản hồi AI ======
def generate_ai_response(message):
    """
    Tạo phản hồi thông minh dựa trên từ khóa và ngữ cảnh
    """
    for keyword, responses in response_data.items():
        if keyword in message.lower():
            return responses[0]  # Lấy câu phản hồi đầu tiên từ responses.json
    
    # Phản hồi mặc định
    return ("Chủ đề này thú vị đấy, nhưng tôi không rõ lắm. "
            "Bạn có thể tìm thêm thông tin trên Google hoặc chia sẻ thêm để tôi hiểu rõ hơn.")

# ====== Trang chính ======
@app.route("/")
def home():
    """
    Trang chính hiển thị giao diện chat và nhật ký cảm xúc
    """
    return render_template("index.html", chat_history=chat_history, emotion_log=emotion_log)

# ====== API xử lý tin nhắn ======
@app.route("/chat", methods=["POST"])
def chat():
    """
    API nhận tin nhắn từ người dùng, phân tích cảm xúc và phản hồi
    """
    data = request.get_json()
    user_message = data.get("message", "").strip()

    # Kiểm tra tin nhắn rỗng
    if not user_message:
        return jsonify({"response": "Tin nhắn của bạn trống. Vui lòng nhập nội dung."}), 400

    # Lưu cảm xúc của người dùng vào nhật ký
    date = datetime.now().strftime("%Y-%m-%d")
    add_emotion_to_log(date, f"Người dùng: {user_message}")
    if analyze_emotion_with_textblob(user_message) != "neutral":
        add_emotion_to_log(date, f"Cảm xúc: {user_message}")

    # Tạo phản hồi từ AI
    bot_response = generate_ai_response(user_message)
    add_emotion_to_log(date, f"AI: {bot_response}")

    # Lưu lịch sử chat
    chat_history.append({"user": user_message, "bot": bot_response})

    # Giới hạn lịch sử chat để tránh tràn bộ nhớ
    if len(chat_history) > 100:
        chat_history.pop(0)

    # Trả về phản hồi và cảm xúc
    return jsonify({"response": bot_response, "chat_history": chat_history})

# ====== API xem nhật ký cảm xúc ======
@app.route("/log_emotion", methods=["GET"])
def log_emotion():
    """
    API để xem nhật ký cảm xúc được lưu trữ
    """
    return jsonify({"emotions": emotion_log, "message": "Emotion log fetched successfully!"})

# ====== Chạy ứng dụng Flask ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



