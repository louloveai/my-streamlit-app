from flask import Flask

# Khởi tạo Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "Ứng dụng của bạn đang chạy thành công!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
