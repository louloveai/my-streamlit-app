from flask import Flask, request, render_template
from transformers import pipeline

# Khởi tạo Flask app
app = Flask(__name__)

# Tải mô hình sẵn để tránh chậm trễ khi khởi động
chatbot = pipeline("text-generation", model="distilgpt2")

@app.route("/")
def home():
    return render_template("index.html", message="Chào mừng bạn đến với AI chữa lành!")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        input_text = request.form["message"]
        response = chatbot(input_text, max_length=100, num_return_sequences=1)[0]["generated_text"]
        return render_template("index.html", message=response)
    except Exception as e:
        return f"Lỗi xử lý: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
