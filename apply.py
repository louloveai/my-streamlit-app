from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Thay YOUR_API_KEY bằng API key thực tế của bạn
openai.api_key = "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"

@app.route("/")
def home():
    welcome_message = "Chào mừng bạn đến với AI Chữa Lành!"
    return render_template("index.html", message=welcome_message)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.form["message"]
        # Sử dụng API ChatCompletion với model text-davinci-003 để kiểm tra
        response = openai.ChatCompletion.create(
            model="text-davinci-003",  # Sử dụng text-davinci-003 thay cho GPT-4
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

