from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load the Hugging Face pipeline
chatbot = pipeline("text-generation", model="distilgpt2")

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = chatbot(user_message, max_length=50, num_return_sequences=1)
    bot_reply = response[0]['generated_text']
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
