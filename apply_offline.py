from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load mô hình trước khi xử lý
chatbot = pipeline("text-generation", model="distilgpt2")  # Thay thế mô hình khác nếu cần

@app.route("/")
def home():
    welcome_message = "Chào mừng đến với AI chữa lành (Offline Mode)"
    return render_template("index.html", message=welcome_message)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.form["message"]
        # Tạo phản hồi từ mô hình
        response = chatbot(user_message, max_length=50, num_return_sequences=1)
        bot_response = response[0]["generated_text"]
        return render_template("index.html", message=bot_response)
    except Exception as e:
        return f"Lỗi khi xử lý request: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
