from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Đảm bảo API key đúng
openai.api_key = "YOUR_API_KEY"

@app.route("/")
def home():
    welcome_message = "Chào mừng bạn đến với AI Chữa Lành!"
    return render_template("index.html", message=welcome_message)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.form["message"]
        # Sử dụng API ChatCompletion đúng phiên bản mới
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Hoặc gpt-4 nếu bạn có quyền truy cập
            messages=[
                {"role": "system", "content": "Bạn là một trợ lý AI chữa lành."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response["choices"][0]["message"]["content"]
        return render_template("index.html", message=bot_response)
    except Exception as e:
        return f"Lỗi khi xử lý request: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
