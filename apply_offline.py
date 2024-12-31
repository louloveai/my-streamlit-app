from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()  # Lấy dữ liệu JSON từ client
    user_message = data.get("message", "")  # Lấy tin nhắn từ client
    ai_response = f"AI trả lời: Bạn vừa nói '{user_message}'"  # Tạo phản hồi đơn giản
    return jsonify({"response": ai_response})  # Trả về JSON chứa phản hồi

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Chạy server Flask

