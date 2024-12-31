from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Chữa Lành</title>
        <style>
            body {
                background-color: #121212;
                color: #fff;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                padding: 20px;
                border-radius: 10px;
                background-color: #1e1e1e;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            }
            input[type="text"] {
                width: 80%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                border: none;
                font-size: 16px;
            }
            button {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Chào mừng đến với AI Chữa Lành!</h1>
            <input id="userMessage" type="text" placeholder="Tin nhắn AI Chữa Lành...">
            <button onclick="sendMessage()">Gửi</button>
            <p id="response"></p>
        </div>
        <script>
            async function sendMessage() {
                const message = document.getElementById("userMessage").value;
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ message })
                });
                const data = await response.json();
                document.getElementById("response").textContent = data.response;
            }
        </script>
    </body>
    </html>
    """

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Tin nhắn không được để trống."}), 400

    ai_response = f"AI trả lời: Bạn vừa nói: {user_message}"
    return jsonify({"response": ai_response}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

