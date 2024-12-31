from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Bộ nhớ tạm thời
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Phản hồi đơn giản từ AI
    if "buồn" in user_message:
        response_message = "Tôi hiểu bạn đang cảm thấy buồn. Bạn muốn tâm sự không?"
    elif "vui" in user_message:
        response_message = "Tôi rất vui khi biết bạn đang hạnh phúc!"
    else:
        response_message = f"Tôi đã nhận được: {user_message}"

    # Lưu vào lịch sử
    chat_history.append({"user": user_message, "ai": response_message})

    return jsonify({"response": response_message})

@app.route("/history", methods=["GET"])
def history():
    return jsonify(chat_history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
