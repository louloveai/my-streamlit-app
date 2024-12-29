from flask import Flask, request, jsonify, render_template
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json
import os
import sqlite3

# Tạo ứng dụng Flask
app = Flask(__name__)

# Load mô hình và tokenizer từ Hugging Face
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Hàm phân tích cảm xúc bằng mô hình có sẵn
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    sentiment = torch.argmax(probs).item()  # Lấy cảm xúc có xác suất cao nhất
    labels = ["Rất tiêu cực", "Tiêu cực", "Trung tính", "Tích cực", "Rất tích cực"]
    return labels[sentiment]

# Route render trang index.html
@app.route("/")
def home():
    return render_template("index.html")

# API phân tích cảm xúc
@app.route("/analyze", methods=["POST"])
def analyze():
    user_input = request.form.get("text", "").strip()
    if not user_input or len(user_input) == 0:  # Check thêm điều kiện độ dài input
        return render_template("index.html", emotion="Lỗi", response="Vui lòng nhập nội dung văn bản để phân tích.")
    
    sentiment = analyze_sentiment(user_input)
    return render_template("index.html", emotion=sentiment, response=f"Cảm xúc của bạn là: {sentiment}")
    
# Khởi động ứng dụng
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Lấy cổng từ biến môi trường hoặc mặc định là 5000
    app.run(host="0.0.0.0", port=port, debug=True)
