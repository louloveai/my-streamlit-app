from flask import Flask, request, jsonify

app = Flask(__name__)

# Một số phản hồi mẫu dựa trên từ khóa
responses = {
    "chào": "Chào bạn! Tôi có thể giúp gì cho bạn hôm nay?",
    "khỏe không": "Tôi là AI nên lúc nào cũng khỏe! Còn bạn thì sao?",
    "tên gì": "Tôi là AI Chữa Lành, sẵn sàng lắng nghe bạn!",
    "buồn": "Hãy chia sẻ thêm, tôi luôn ở đây để lắng nghe bạn.",
    "vui": "Thật tuyệt khi nghe điều đó! Hãy tiếp tục giữ năng lượng tích cực nhé!"
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").lower()
    
    # Kiểm tra từ khóa trong tin nhắn
    for keyword, response in responses.items():
        if keyword in user_message:
            return jsonify({"response": response})
    
    # Phản hồi mặc định nếu không tìm thấy từ khóa
    default_response = "Cảm ơn bạn đã chia sẻ. Tôi sẽ cố gắng hiểu thêm về bạn!"
    return jsonify({"response": default_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

