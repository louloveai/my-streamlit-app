from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load model
chatbot = pipeline("text-generation", model="distilgpt2")

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    response = chatbot(user_message, max_length=50, num_return_sequences=1)
    reply = response[0]['generated_text']
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
