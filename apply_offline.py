from flask import Flask, request, jsonify, render_template
from datetime import datetime
from textblob import TextBlob
import json

app = Flask(__name__)

# Lưu trữ lịch sử chat và nhật ký cảm xúc
chat_history = []  # Lịch sử chat
emotion_log = {}  # Lưu cảm xúc theo ngày

# Tải dữ liệu phản hồi từ file JSON
with open("responses.json", "r", encoding="utf-8") as file:
    response_data = json.load(file)

# Hàm phân tích cảm xúc cơ bản
def analyze_emotion_with_textblob(message):
    analysis = TextBlob(message)
    polarity = analysis.sentiment.polarity
    if polarity < -0.3:
        return "negative"
    elif polarity > 0.3:
        return "positive"
    return "neutral"

# Hàm lưu cảm xúc vào nhật ký theo ngày
def add_emotion_to_log(date, message):
    if date not in emotion_log:
        emotion_log[date] = []
    if message not in emotion_log[date]:  # Tránh lưu trùng lặp
        emotion_log[date].append(message)

# Hàm tạo phản hồi AI thông minh
def generate_ai_response(message):
    # Phản hồi thông minh dựa trên từ khóa
    if "buồn" in message.lower():
        return ("Tôi rất tiếc khi nghe điều này. "
                "Bạn biết không, mỗi người đều có hành trình riêng của mình. "
                "Hãy chia sẻ thêm với tôi nhé, tôi luôn ở đây để lắng nghe.")
    elif "vui" in message.lower():
        return ("Tuyệt vời! Tôi rất vui khi nghe điều này. "
                "Hãy giữ niềm vui này và lan tỏa nó đến mọi người xung quanh.")
    elif "tức giận" in message.lower():
        return ("Tôi hiểu cảm giác của bạn. "
                "Hãy thử hít thở sâu vài lần để cảm thấy dễ chịu hơn. "
                "Bạn muốn chia sẻ thêm về tình huống không?")
    elif "cô đơn" in message.lower():
        return ("Bạn không cô đơn đâu, tôi luôn ở đây để trò chuyện với bạn. "
                "Mọi người đều cần ai đó để lắng nghe, và tôi sẵn sàng.")
    elif "lo lắng" in message.lower():
        return ("Hãy chia sẻ với tôi những điều bạn đang lo lắng. "
                "Biết đâu việc nói ra sẽ giúp bạn cảm thấy nhẹ nhàng hơn.")
    elif "?" in message:
        return ("Chủ đề này thú vị đấy, nhưng tôi không rõ lắm. "
                "Bạn có thể tìm thêm thông tin trên Google hoặc chia sẻ thêm để tôi hiểu rõ hơn.")
    
    # Phản hồi mặc định
    return "Tôi luôn sẵn sàng lắng nghe bạn. Hãy chia sẻ thêm nhé!"

# Trang chính
@app.route("/")
def home():
    return render_template("index.html", chat_history=chat_history, emotion_log=emotion_log)

# API xử lý tin nhắn người dùng
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    # Kiểm tra tin nhắn trống
    if not user_message:
        return jsonify({"response": "Tin nhắn của bạn trống. Vui lòng nhập nội dung."}), 400

    # Phân tích cảm xúc và lưu nếu phát hiện
    date = datetime.now().strftime("%Y-%m-%d")
    add_emotion_to_log(date, f"Người dùng: {user_message}")
    if analyze_emotion_with_textblob(user_message) != "neutral":
        add_emotion_to_log(date, f"Cảm xúc: {user_message}")

    # Tạo phản hồi AI
    bot_response = generate_ai_response(user_message)
    add_emotion_to_log(date, f"AI: {bot_response}")

    # Lưu vào lịch sử chat
    chat_history.append({"user": user_message, "bot": bot_response})

    # Giới hạn lịch sử chat để tránh tràn bộ nhớ
    if len(chat_history) > 100:
        chat_history.pop(0)

    return jsonify({"response": bot_response, "chat_history": chat_history})

# API xem nhật ký cảm xúc
@app.route("/log_emotion", methods=["GET"])
def log_emotion():
    return jsonify({"emotions": emotion_log, "message": "Emotion log fetched successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



