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
    if message not in emotion_log[date]:  # Tránh lưu trùng lặp
        emotion_log[date].append(message)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Phân tích cảm xúc và lưu nếu cần
    if analyze_emotion(user_message):
        add_emotion_to_log(user_message)
    
    # Tạo phản hồi AI
    bot_response = generate_ai_response(user_message)
    
    # Lưu lịch sử chat
    chat_history.append({"user": user_message, "bot": bot_response})
    
    return jsonify({"response": bot_response})
    
# Hàm tạo phản hồi AI thông minh
def generate_ai_response(message):
    # Các phản hồi tâm lý chữa lành
    if "buồn" in message.lower():
        return "Tôi rất tiếc khi nghe điều này. Nhưng bạn biết không, cảm xúc buồn cũng là một phần của cuộc sống và giúp chúng ta trưởng thành hơn."
    elif "vui" in message.lower():
        return "Tôi rất vui khi nghe điều này! Chúc bạn luôn giữ được niềm vui và năng lượng tích cực này nhé!"
    elif "mệt mỏi" in message.lower() or "stress" in message.lower():
        return "Có vẻ bạn đang gặp khó khăn. Hãy thử nghỉ ngơi, thư giãn một chút hoặc chia sẻ thêm với tôi nhé."
    elif "cô đơn" in message.lower():
        return "Bạn không cô đơn đâu. Tôi luôn ở đây để lắng nghe bạn. Hãy chia sẻ bất cứ điều gì bạn muốn nhé."
    elif "lo lắng" in message.lower():
        return "Lo lắng là cảm xúc bình thường khi đối mặt với điều mới mẻ. Nhưng tôi tin rằng bạn có thể vượt qua được. Hãy chia sẻ thêm với tôi."
    elif "không biết làm gì" in message.lower():
        return "Hãy bắt đầu với điều nhỏ nhất mà bạn cảm thấy có thể làm. Mỗi bước nhỏ đều là một bước tiến lớn về lâu dài."
 
    # Phản hồi từ chối khéo
    if "?" in message:
        return "Chủ đề này thú vị đấy, nhưng mình không rõ lắm. Bạn có thể tìm thêm thông tin qua Google để có câu trả lời chính xác hơn."
    
    # Phản hồi mặc định
    return "Tôi đã nhận được tin nhắn của bạn. Hãy chia sẻ thêm nhé, tôi luôn ở đây để lắng nghe."

# Tích hợp logic phản hồi trong /chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Phân tích cảm xúc và lưu
    if analyze_emotion(user_message):
        add_emotion_to_log(user_message)
    
    # Tạo phản hồi
    bot_response = generate_ai_response(user_message)
    chat_history.append({"user": user_message, "bot": bot_response})
    
    return jsonify({"response": bot_response})


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
    user_message = data.get("message", "")
    if not data or "message" not in data:
        return jsonify({"error": "Invalid data"}), 400

    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"response": "Tin nhắn của bạn trống. Vui lòng nhập nội dung."}), 400

    # Phân tích và lưu cảm xúc nếu phát hiện
    add_emotion_to_log(user_message)

    # Tạo phản hồi AI
    bot_response = generate_ai_response(user_message)

    # Lưu vào lịch sử chat
    chat_history.append({"user": user_message, "bot": bot_response})

    return jsonify({"response": bot_response})
    if not data or "message" not in data:
        return jsonify({"error": "Invalid data"}), 400

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




