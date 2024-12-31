from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Lưu trữ lịch sử chat và nhật ký cảm xúc
chat_history = []
emotion_log = {}  # Lưu cảm xúc theo ngày

# Hàm phân tích cảm xúc
def analyze_emotion(message):
    important_emotions = ["buồn", "vui", "tức giận", "cô đơn", "lo lắng"]
    for emotion in important_emotions:
        if emotion in message.lower():
            return True
    return False

# Hàm lưu cảm xúc vào nhật ký theo ngày
def add_emotion_to_log(message):
    date = datetime.now().strftime("%Y-%m-%d")  # Ngày hiện tại
    if date not in emotion_log:
        emotion_log[date] = []
    emotion_log[date].append(message)

# Hàm tạo phản hồi AI thông minh
def generate_ai_response(message):
    # Phản hồi thông minh dựa trên từ khóa
    if "buồn" in message.lower():
        return "Tôi rất tiếc khi nghe điều này. Bạn có muốn chia sẻ thêm không?"
    elif "vui" in message.lower():
        return "Tôi rất vui khi nghe điều này! Chúc bạn luôn giữ được niềm vui."
    elif "tức giận" in message.lower():
        return "Tôi hiểu cảm giác của bạn. Hãy thử hít thở sâu và thư giãn nhé."
    elif "cô đơn" in message.lower():
        return "Bạn không cô đơn đâu, tôi luôn ở đây để trò chuyện với bạn."
    elif "lo lắng" in message.lower():
        return "Hãy chia sẻ với tôi để bạn cảm thấy nhẹ nhàng hơn nhé."
    return "Tôi đã nhận được tin nhắn của bạn!"

# Trang chính
@app.route("/")
def home():
    return render_template("index.html", chat_history=chat_history, emotion_log=emotion_log)
    
# Xử lý tin nhắn người dùng
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Phân tích và lưu cảm xúc nếu cần
    if analyze_emotion(user_message):
        add_emotion_to_log(user_message)
    
    # Tạo phản hồi AI
    bot_response = generate_ai_response(user_message)
    
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
    emotion = data.get("emotion")
    if date in emotion_log and emotion in emotion_log[date]:
        emotion_log[date].remove(emotion)
        return jsonify({"message": "Emotion deleted successfully!"})
    return jsonify({"message": "Emotion not found!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

