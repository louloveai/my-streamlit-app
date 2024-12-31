from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head><title>AI Chữa Lành</title></head>
    <body style="background-color: #1e1e1e; color: #ffffff; font-family: Arial, sans-serif; text-align: center;">
        <h1>Chào mừng đến với AI Chữa Lành!</h1>
        <form action="/chat" method="post" style="margin-top: 20px;">
            <input type="text" name="message" placeholder="Nhập tin nhắn của bạn..." 
            style="padding: 10px; width: 70%; border-radius: 5px; border: none;"/>
            <button type="submit" style="padding: 10px; background-color: #008CBA; color: white; 
            border: none; border-radius: 5px; cursor: pointer;">Gửi</button>
        </form>
    </body>
    </html>
    """

@app.route('/chat', methods=['POST'])
def chat():
    # Lấy dữ liệu từ người dùng
    data = request.form.get('message', '')
    if not data:
        return jsonify({"response": "Vui lòng nhập tin nhắn!"})
    
    # Phản hồi đơn giản
    return jsonify({"response": f"AI trả lời: Bạn vừa nói: {data}"})
