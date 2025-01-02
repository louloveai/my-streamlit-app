import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Tải mô hình đã huấn luyện và vectorizer
model = joblib.load("chatbot_model.pkl")
vectorizer = TfidfVectorizer()
vectorizer.fit(pd.read_csv("chat_history.csv")["user_message"])

# Kiểm tra mô hình trên dữ liệu thực tế
def test_model():
    while True:
        user_message = input("Nhập tin nhắn người dùng (gõ 'exit' để thoát): ")
        if user_message.lower() == "exit":
            break
        vectorized_message = vectorizer.transform([user_message])
        predicted_response = model.predict(vectorized_message)[0]
        print(f"AI phản hồi: {predicted_response}")

if __name__ == "__main__":
    print("Bắt đầu kiểm tra mô hình...")
    test_model()
