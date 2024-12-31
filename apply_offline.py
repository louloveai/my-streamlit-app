from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
emotions = []  # Tạm thời lưu cảm xúc trong danh sách

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/log_emotion', methods=['POST'])
def log_emotion():
    emotion = request.form.get('emotion', '')
    if emotion:
        emotions.append(emotion)
        return jsonify({"message": "Emotion logged successfully!", "emotions": emotions}), 200
    return jsonify({"message": "No emotion provided!"}), 400

@app.route('/get_emotions', methods=['GET'])
def get_emotions():
    return jsonify({"emotions": emotions}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
