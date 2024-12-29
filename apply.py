from flask import Flask, request, render_template
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from dotenv import load_dotenv
import os
import time

# Load API Key từ file .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY không được tìm thấy trong file .env. Vui lòng kiểm tra lại.")

# Tải mô hình và tokenizer từ Hugging Face
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"  # Mô hình nhẹ hơn, phù hợp với phân loại cảm xúc
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Tạo ứng dụng Flask
app = Flask(__name__)

# Hàm phân tích cảm xúc
def analyze_sentiment(text):
    try:
        start_time = time.time()
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

        # Nhãn cảm xúc
        labels = ["Tiêu cực", "Tích cực"]
        sentiment = torch.argmax(probs).item()

        print(f"Thời gian xử lý: {time.time() - start_time:.2f} giây")
        return labels[sentiment]
    except Exception as e:
        print("Error during sentiment analysis:", e)
        return "Không xác định"

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

    # Gọi hàm phân tích cảm xúc
    emotion = analyze_sentiment(user_input)
    return render_template("index.html", emotion=emotion, response=f"Cảm xúc của bạn là: {emotion}")

# Khởi động ứng dụng Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Lấy cổng từ biến môi trường hoặc mặc định là 5000
    app.run(host="0.0.0.0", port=port, debug=False)

