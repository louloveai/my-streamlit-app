from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Bộ nhớ tạm để lưu cảm xúc người dùng
emotion_log = []

# Route chính hiển thị giao diện người dùng
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Healing</title>
        <style>
            body {
                background-color: black;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            h1 {
                font-size: 2.5em;
                margin-top: 20px;
            }
            textarea {
                width: 80%;
                height: 100px;
                border: 1px solid white;
                border-radius: 10px;
                background-color: black;
                color: white;
                font-size: 1em;
                padding: 10px;
                margin-bottom: 20px;
            }
            button {
                background-color: white;
                color: black;
                border: none;
                padding: 10px 20px;
                border-radius: 30px;
                font-size: 1em;
                cursor: pointer;
            }
            button:focus {
                outline: none;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                margin: 10px 0;
                font-size: 1.2em;
            }
        </style>
        <script>
            async function logEmotion() {
                const textarea = document.getElementById('emotion-input');
                const emotion = textarea.value.trim();
                if (!emotion) return;

                const response = await fetch('/log_emotion', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ emotion }),
                });

                const data = await response.json();
                if (data.message) {
                    const emotionLog = document.getElementById('emotion-log');
                    const listItem = document.createElement('li');
                    listItem.textContent = data.message;
                    emotionLog.appendChild(listItem);
                    textarea.value = '';
                }
            }

            document.addEventListener('DOMContentLoaded', () => {
                const textarea = document.getElementById('emotion-input');
                textarea.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        logEmotion();
                    }
                });
            });
        </script>
    </head>
    <body>
        <h1>Welcome to AI Healing</h1>
        <textarea id="emotion-input" placeholder="Mô tả cảm xúc của bạn..."></textarea>
        <br>
        <button onclick="logEmotion()">Gửi</button>
        <h2>Nhật ký cảm xúc:</h2>
        <ul id="emotion-log">
            {% for emotion in emotions %}
            <li>{{ emotion }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """

# API để ghi cảm xúc
@app.route('/log_emotion', methods=['POST'])
def log_emotion():
    data = request.get_json()
    emotion = data.get('emotion', '').strip()
    if emotion:
        emotion_log.append(emotion)
        return jsonify({
            "emotions": emotion_log,
            "message": f"Cảm xúc của bạn đã được ghi nhận: {emotion}"
        })
    return jsonify({
        "message": "Không có cảm xúc nào được gửi."
    }), 400

# Chạy app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
