from flask import Flask, render_template, request

# Khởi tạo Flask app
app = Flask(__name__)

# Các phản hồi mẫu
predefined_responses = {
    "chào": "Xin chào! Tôi có thể giúp gì cho bạn?",
    "buồn": "Tôi rất tiếc khi nghe điều đó. Bạn muốn chia sẻ gì không?",
    "vui": "Thật tuyệt! Chúc bạn luôn giữ được niềm vui này!",
    "cảm ơn": "Không có gì! Tôi luôn sẵn sàng giúp bạn!",
    "hỏi": "Bạn có thể đặt bất kỳ câu hỏi nào, tôi sẽ cố gắng trả lời!"
}

@app.route("/")
def home():
    welcome_message = "Chào mừng đến với AI Chữa Lành!"
    return render_template("index.html", message=welcome_message)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Lấy tin nhắn từ người dùng
        user_message = request.form["message"].lower()
        # Lấy phản hồi dựa trên input
        response = predefined_responses.get(user_message, "Cảm ơn bạn đã nhắn tin. Tôi đang lắng nghe.")
        return render_template("index.html", bot_response=response)
    except Exception as e:
        return f"Lỗi xảy ra: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
