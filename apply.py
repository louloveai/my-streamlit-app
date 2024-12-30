from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Đảm bảo API key đúng
openai.api_key = "YOUR_API_KEY"

@app.route("/")
def home():
    welcome_message = "Chào mừng bạn đến với AI Chữa Lành!"
    return render_template("index.html", message=welcome_message)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.form["message"]
        # Sử dụng OpenAI API với model GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response["choices"][0]["message"]["content"]
        return render_template("index.html", message=bot_response)
    except Exception as e:
        return f"Lỗi khi xử lý request: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
