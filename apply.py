from flask import Flask, request, render_template

# Khởi tạo Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "Ứng dụng của bạn đang chạy thành công!"

# Chạy ứng dụng Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
