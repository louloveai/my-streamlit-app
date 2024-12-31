from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Khởi tạo pipeline sử dụng CPU
chatbot = pipeline("text-generation", model="distilgpt2", device=-1)

@app.route("/")
def home():
    return render_template("index.html", message="Chào mừng đến với AI!")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"]
    response = chatbot(user_message, max_length=100, num_return_sequences=1)[0]["generated_text"]
    return render_template("index.html", message=user_message, bot_response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
