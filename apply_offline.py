from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Preload the model during initialization with max token limit
chatbot = pipeline("text-generation", model="distilgpt2", device=0, max_length=50)  # Giới hạn 50 token

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.form["message"]
        # Generate response from the model
        response = chatbot(user_input, max_length=50)[0]["generated_text"]
        return render_template("index.html", bot_response=response)
    except Exception as e:
        return f"Lỗi khi xử lý request: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
