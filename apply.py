from flask import Flask, request, render_template

# Tạo ứng dụng Flask
app = Flask(__name__)

# Trang chính
@app.route("/")
def home():
    return render_template("index.html")

# API xử lý
@app.route("/analyze", methods=["POST"])
def analyze():
    user_input = request.form.get("text", "").strip()
    if not user_input:
        return render_template("index.html", emotion="Lỗi", response="Vui lòng nhập nội dung.")
    
    # Phản hồi đơn giản
    return render_template("index.html", emotion="Trung tính", response=f"Nội dung nhận được: {user_input}")

# Chạy ứng dụng
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

