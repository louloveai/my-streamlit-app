from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# API key mới
openai.api_key = "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"

@app.route("/")
def home():
    welcome_message = "Chào mừng bạn đến với AI Chữa Lành!"
    return render_template("index.html", message=welcome_message)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.form["message"]
        # Gọi API ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Đảm bảo mô hình có quyền sử dụng
            messages=[
                {"role": "system", "content": "Bạn là một AI hỗ trợ chữa lành."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response['choices'][0]['message']['content'].strip()
        return render_template("index.html", message=bot_response)
    except Exception as e:
        return f"Lỗi khi xử lý request: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

