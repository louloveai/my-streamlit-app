from flask import Flask, render_template, request
import openai

app = Flask(__name__)

openai.api_key = "YOUR_API_KEY"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form.get("message")
    if user_message:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_message,
            max_tokens=150
        )
        bot_response = response.choices[0].text.strip()
    else:
        bot_response = "Vui lòng nhập tin nhắn của bạn!"
    return render_template("index.html", message=bot_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

