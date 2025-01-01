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
    
    # Chuyển hướng thông minh khi gặp câu hỏi ngoài khả năng
    elif "?" in message:
        return "Chủ đề này thú vị đấy, nhưng tôi không rõ lắm. Bạn có thể tìm thêm thông tin trên Google hoặc chia sẻ thêm để tôi hiểu rõ hơn."
    
    # Trường hợp không xác định
    return "Cảm ơn bạn đã chia sẻ. Tôi luôn sẵn sàng lắng nghe bạn."

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

# Hàm lưu toàn bộ tin nhắn và cảm xúc vào nhật ký
def add_to_emotion_log(date, message):
    if date not in emotion_log:
        emotion_log[date] = []
    emotion_log[date].append(message)
Sửa logic trong hàm /chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Invalid data"}), 400
    user_message = data.get("message", "")

    # Lưu tin nhắn vào nhật ký cảm xúc
    date = datetime.now().strftime("%Y-%m-%d")
    add_to_emotion_log(date, f"Người dùng: {user_message}")
    
    # Phân tích cảm xúc và lưu nếu cần
    if analyze_emotion(user_message):
        add_to_emotion_log(date, f"Cảm xúc: {user_message}")

    # Tạo phản hồi AI
    bot_response = generate_ai_response(user_message)
    add_to_emotion_log(date, f"AI: {bot_response}")
    
    # Lưu vào lịch sử chat
    chat_history.append({"user": user_message, "bot": bot_response})
    
    return jsonify({"response": bot_response})
  # Cải thiện API xem nhật ký cảm xúc: 
@app.route("/log_emotion")
def log_emotion():
    return jsonify({"emotions": emotion_log, "message": "Emotion log fetched successfully!"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()  # Đảm bảo dữ liệu POST là JSON
    if not data or "message" not in data:
        return jsonify({"error": "Invalid data"}), 400
    user_message = data.get("message", "")
    
    # Phân tích và lưu cảm xúc nếu cần
    if analyze_emotion(user_message):
        add_emotion_to_log(user_message)
    
    # Tạo phản hồi AI
    bot_response = generate_ai_response(user_message)
    
    # Lưu vào lịch sử chat
    chat_history.append({"user": user_message, "bot": bot_response})
    
    return jsonify({"response": bot_response})
   
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
    
    # Chuyển hướng thông minh khi gặp câu hỏi ngoài khả năng
    elif "?" in message:
        return "Chủ đề này thú vị đấy, nhưng tôi không rõ lắm. Bạn có thể tìm thêm thông tin trên Google hoặc chia sẻ thêm để tôi hiểu rõ hơn."
     return ("Chủ đề này thú vị đấy, nhưng tôi không rõ lắm. "
            "Bạn có thể Google giúp để có thêm thông tin chính xác hơn.")
    # Trường hợp không xác định
    return "Cảm ơn bạn đã chia sẻ. Tôi luôn sẵn sàng lắng nghe bạn."

    # Phản hồi từ chối khéo
    if "?" in message:
        return "Chủ đề này thú vị đấy, nhưng mình không rõ lắm. Bạn có thể tìm thêm thông tin qua Google để có câu trả lời chính xác hơn."
    
    # Phản hồi mặc định
    return "Tôi đã nhận được tin nhắn của bạn. Hãy chia sẻ thêm nhé, tôi luôn ở đây để lắng nghe."
    # Cập nhật logic trong hàm /chat
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Invalid data"}), 400
    user_message = data.get("message", "")

    # Phân tích và lưu cảm xúc nếu cần
    date = datetime.now().strftime("%Y-%m-%d")
    add_to_emotion_log(date, f"Người dùng: {user_message}")
    if analyze_emotion(user_message):
        add_to_emotion_log(date, f"Cảm xúc: {user_message}")

    # Tạo phản hồi AI
    bot_response = generate_ai_response(user_message)
    add_to_emotion_log(date, f"AI: {bot_response}")
    
    # Lưu vào lịch sử chat
    chat_history.append({"user": user_message, "bot": bot_response})
    
    return jsonify({"response": bot_response})

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




