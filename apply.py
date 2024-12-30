from flask import Flask, render_template, request
import openai

app = Flask(__name__)

openai.api_key = "YOUR_API_KEY"

@app.route("/")
def home():
    welcome_message = "Chào mừng bạn đến với ứng dụng của chúng tôi!"
    return render_template("index.html", message=welcome_message)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]
    if user_message.strip() == "":
        bot_response = "Vui lòng nhập tin nhắn hợp lệ."
    else:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_message,
            max_tokens=150
        )
        bot_response = response.choices[0].text.strip()
    return render_template("index.html", message=bot_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
