from flask import Flask, request, jsonify, render_template
from datetime import datetime
from textblob import TextBlob

app = Flask(__name__)

# Lưu trữ lịch sử chat, cảm xúc và trạng thái hội thoại
chat_history = []
emotion_log = {}  # Lưu cảm xúc theo ngày
conversation_state = {}  # Trạng thái hội thoại theo user ID

# Hàm phân tích cảm xúc nâng cao
def analyze_emotion(message):
    sentiment = TextBlob(message).sentiment
    if sentiment.polarity > 0.5:
        return "positive"
    elif sentiment.polarity < -0.5:
        return "negative"
    return "neutral"

# Hàm lưu cảm xúc vào nhật ký theo ngày
def add_emotion_to_log(message, emotion_type):
    date = datetime.now().strftime("%Y-%m-%d")  # Ngày hiện tại
    if date not in emotion_log:
        emotion_log[date] = []
    emotion_log[date].append({"message": message, "emotion": emotion_type})

# Hàm gợi ý hành động dựa trên cảm xúc
def generate_suggestions(emotion_type):
    if emotion_type == "positive":
        return "Bạn có muốn ghi lại niềm vui này vào nhật ký cảm xúc không?"
    elif emotion_type == "negative":
        return "Hãy thử một bài tập thở sâu hoặc nghe nhạc thư giãn nhé!"
    return "Hãy chia sẻ thêm, tôi muốn lắng nghe bạn."

# Hàm tạo phản hồi AI thông minh
def generate_ai_response(message, user_id):
    if user_id not in conversation_state:
        conversation_state[user_id] = "init"

    # Phản hồi theo trạng thái hội thoại
    if conversation_state[user_id] == "init":
        emotion = analyze_emotion(message)
        if emotion == "negative":
            conversation_state[user_id] = "ask_more_negative"
            return "Tôi rất tiếc khi nghe điều này. Bạn có muốn chia sẻ thêm không?"
        elif emotion == "positive":
            conversation_state[user_id] = "ask_more_positive"
            return "Thật tuyệt khi nghe điều đó! Bạn muốn chia sẻ thêm gì không?"
        else:
            return "Tôi đang nghe bạn, hãy kể thêm nhé!"

    elif conversation_state[user_id] == "ask_more_negative":
        conversation_state[user_id] = "init"
        return "Cảm ơn bạn đã chia sẻ. Tôi hiểu và sẵn sàng lắng nghe bạn thêm."

    elif conversation_state[user_id] == "ask_more_positive":
        conversation_state[user_id] = "init"
        return "Thật tuyệt vời! Hãy giữ niềm vui này nhé."

    return "Tôi đã nhận được tin nhắn của bạn!"

# Trang chính
@app.route("/")
def home():
    # Truyền cả emotion_log và chat_history vào template
    return render_template("index.html", chat_history=chat_history, emotion_log=emotion_log)

# Xử lý tin nhắn người dùng
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()  # Đảm bảo dữ liệu POST là JSON
    if not data or "message" not in data:
        return jsonify({"error": "Invalid data"}), 400
    user_message = data.get("message", "")
    user_id = data.get("user_id", "default_user")  # Sử dụng user ID mặc định

    # Phân tích cảm xúc và lưu nếu cần
    emotion = analyze_emotion(user_message)
    add_emotion_to_log(user_message, emotion)

    # Tạo phản hồi AI
    bot_response = generate_ai_response(user_message, user_id)

    # Lưu vào lịch sử chat
    chat_history.append({"user": user_message, "bot": bot_response})

    return jsonify({"response": bot_response})

# API lấy nhật ký cảm xúc
@app.route("/log_emotion")
def log_emotion():
    return jsonify({"emotions": emotion_log, "message": "Emotion log fetched successfully!"})

# API xóa cảm xúc
@app.route('/delete_emotion', methods=['POST'])
def delete_emotion():
    data = request.get_json()
    date = data.get("date")
    emotion_entry = data.get("emotion")
    if date in emotion_log:
        emotion_log[date] = [e for e in emotion_log[date] if e["emotion"] != emotion_entry]
        return jsonify({"message": "Emotion deleted successfully!"})
    return jsonify({"message": "Emotion not found!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



