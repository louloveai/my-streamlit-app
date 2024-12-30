from flask import Flask, render_template

app = Flask(__name__)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

@app.route("/")
def home():
    welcome_message = "Chào mừng bạn đến với ứng dụng của chúng tôi!"
    return render_template("index.html", message=welcome_message)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]
    bot_response = "Cảm ơn bạn đã nhắn tin. Đây là phản hồi mẫu."
    return render_template("index.html", message=bot_response)

import openai

openai.api_key = "YOUR_API_KEY"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_message,
        max_tokens=150
    )
    bot_response = response.choices[0].text.strip()
    return render_template("index.html", message=bot_response)
