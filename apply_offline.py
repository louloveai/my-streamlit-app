from flask import Flask, request, jsonify, render_template
from datetime import datetime
from textblob import TextBlob
import json
import os

app = Flask(__name__)

# ====== Cấu hình Kaggle API ======
os.environ['KAGGLE_CONFIG_DIR'] = "./config"

# Kiểm tra kết nối với Kaggle API
try:
    os.system("kaggle datasets list")
    print("Kết nối Kaggle API thành công!")
except Exception as e:
    print(f"Lỗi kết nối Kaggle API: {e}")

# Tải một bộ dữ liệu từ Kaggle (ví dụ: HappyDB)
os.system("kaggle datasets download -d iarunava/happydb -p ./data")

# Giải nén dữ liệu
os.system("unzip -o ./data/happydb.zip -d ./data")

# ====== Lưu trữ lịch sử chat và nhật ký cảm xúc ======
chat_history = []  # Lịch sử chat giữa người dùng và AI
emotion_log = {}  # Lưu cảm xúc theo ngày

# ====== Tải dữ liệu phản hồi từ file JSON ======
try:
    with open("responses.json", "r", encoding="utf-8") as file:
        response_data = json.load(file)
except FileNotFoundError:
    response_data = {}  # Nếu không tìm thấy file, sử dụng dữ liệu rỗng để tránh lỗi

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
    
    # Phản hồi mặc định khi không tìm thấy từ khóa
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
    sentiment = analyze_emotion_with_textblob(user_message)
    if sentiment != "neutral":
        add_emotion_to_log(date, f"Cảm xúc: {sentiment}")

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
    # Định dạng dữ liệu để dễ hiển thị trên giao diện
    formatted_log = {
        date: {"entries": emotions, "count": len(emotions)}
        for date, emotions in emotion_log.items()
    }
    return jsonify({"emotions": formatted_log, "message": "Emotion log fetched successfully!"})

# ====== Chạy ứng dụng Flask ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



