from flask import Flask, request, render_template
import requests
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY không được tìm thấy trong file .env. Vui lòng kiểm tra lại.")

# Tạo ứng dụng Flask
app = Flask(__name__)

# Hàm gửi yêu cầu tới Hugging Face API
def analyze_sentiment(text):
    API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {"inputs": text}
    
    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    
    if "error" in result:
        return "Không xác định", "Có lỗi xảy ra khi xử lý văn bản."
    
    # Phân tích kết quả
    labels = ["Rất tiêu cực", "Tiêu cực", "Trung tính", "Tích cực", "Rất tích cực"]
    sentiment = result[0]  # Lấy kết quả đầu tiên
    predicted_label = max(sentiment, key=lambda x: x['score'])  # Dự đoán cảm xúc
    return predicted_label['label'], f"Dự đoán cảm xúc: {predicted_label['label']}"

# Route render trang index.html
@app.route("/")
def home():
    return render_template("index.html")

# API phân tích cảm xúc
@app.route("/analyze", methods=["POST"])
def analyze():
    user_input = request.form.get("text", "").strip()
    if not user_input:
        return render_template("index.html", emotion="Lỗi", response="Vui lòng nhập nội dung văn bản để phân tích.")
    
    emotion, response = analyze_sentiment(user_input)
    return render_template("index.html", emotion=emotion, response=response)

# Khởi động ứng dụng
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Lấy cổng từ biến môi trường hoặc mặc định là 5000
    app.run(host="0.0.0.0", port=port, debug=True)

import gradio as gr
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load mô hình và tokenizer từ Hugging Face
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Hàm phân tích cảm xúc
def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    labels = ["Rất tiêu cực", "Tiêu cực", "Trung tính", "Tích cực", "Rất tích cực"]
    sentiment = torch.argmax(probs).item()
    return labels[sentiment]

# Tạo giao diện Gradio
def analyze(input_text):
    result = analyze_sentiment(input_text)
    return f"Cảm xúc phân tích: {result}"

interface = gr.Interface(
    fn=analyze,
    inputs=gr.Textbox(label="Nhập văn bản của bạn:"),
    outputs=gr.Textbox(label="Kết quả phân tích:")
)

# Chạy ứng dụng
if __name__ == "__main__":
    interface.launch()

