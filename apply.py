from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# Lấy API key từ biến môi trường
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    welcome_message = "Chào mừng bạn đến với AI Chữa Lành!"
    return render_template("index.html", message=welcome_message)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.form["message"]
        # Sử dụng API ChatCompletion đúng phiên bản
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Bạn có thể dùng GPT-3.5-turbo hoặc GPT-4 (nếu có quyền truy cập)
            messages=[
                {"role": "system", "content": "Bạn là một AI hỗ trợ chữa lành."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response["choices"][0]["message"]["content"].strip()
        return render_template("index.html", message=bot_response)
    except Exception as e:
        return f"Lỗi khi xử lý request: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

