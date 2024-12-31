from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Tạo pipeline với mô hình ngôn ngữ offline
chatbot = pipeline("text-generation", model="distilgpt2")

@app.route("/")
def home():
    return render_template("index.html", message="Chào mừng đến với AI Chữa Lành!")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.form["message"]
        response = chatbot(user_message, max_length=50, num_return_sequences=1)
        bot_response = response[0]["generated_text"]
        return render_template("index.html", message=bot_response)
    except Exception as e:
        return f"Lỗi khi xử lý: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
