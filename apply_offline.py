from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    ai_response = f"AI trả lời: Bạn vừa nói: {user_message}"  # Logic AI đơn giản
    return jsonify({"response": ai_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


