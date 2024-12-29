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
import requests

# Hàm gửi yêu cầu tới Hugging Face API
def analyze_sentiment(text):
    API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
    headers = {"Authorization": f"Bearer YOUR_API_TOKEN"}
    data = {"inputs": text}
    
    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    
    if "error" in result:
        return "Không xác định", "Có lỗi xảy ra khi xử lý văn bản."
    
    # Phân tích kết quả
    labels = ["Rất tiêu cực", "Tiêu cực", "Trung tính", "Tích cực", "Rất tích cực"]
    sentiment = result[0]  # Lấy kết quả đầu tiên
    predicted_label = max(sentiment, key=lambda x: x['score'])  # Dự đoán cảm xúc
    label_index = sentiment.index(predicted_label)
    return labels[label_index]
    
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
