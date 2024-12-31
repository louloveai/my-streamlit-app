from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Lưu trữ lịch sử chat và nhật ký cảm xúc
chat_history = []
emotion_log = {}

# Hàm phân tích cảm xúc
def analyze_emotion(message):
    important_emotions = ["buồn", "vui", "tức giận", "cô đơn", "lo lắng"]
    for emotion in important_emotions:
        if emotion in message.lower():
            return True
    return False

# Hàm thêm cảm xúc vào nhật ký theo ngày
def add_emotion_to_log(message):
    date = datetime.now().strftime("%Y-%m-%d")
    if date not in emotion_log:
        emotion_log[date] = []
    emotion_log[date].append(message)

@app.route("/")
def home():
    return render_template("index.html", chat_history=chat_history, emotions=emotion_log)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Phân tích và xử lý cảm xúc
    if analyze_emotion(user_message):
        add_emotion_to_log(user_message)  # Lưu cảm xúc vào nhật ký
    
    # Lưu lịch sử chat
    bot_response = f"AI trả lời: {user_message}"
    chat_history.append({"user": user_message, "bot": bot_response})
    
    return jsonify({"response": bot_response})

@app.route("/log_emotion")
def log_emotion():
    return jsonify({"emotions": emotion_log, "message": "Emotion log fetched successfully!"})

@app.route('/delete_emotion', methods=['POST'])
def delete_emotion():
    data = request.get_json()
    date = data.get("date")
    emotion = data.get("emotion")
    if date in emotion_log and emotion in emotion_log[date]:
        emotion_log[date].remove(emotion)
        return jsonify({"message": "Emotion deleted successfully!"})
    return jsonify({"message": "Emotion not found!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
