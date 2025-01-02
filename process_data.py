import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Đọc file CSV chứa lịch sử chat
data = pd.read_csv("chat_history.csv")

# Loại bỏ các dòng dữ liệu bị trống hoặc không hợp lệ
data.dropna(inplace=True)
print(f"Dữ liệu sau khi làm sạch: {len(data)} dòng")

# Chuẩn bị dữ liệu đầu vào (input) và đầu ra (output)
X = data["user_message"]  # Tin nhắn từ người dùng
y = data["bot_response"]  # Phản hồi từ AI

# Chuyển đổi văn bản thành số (TF-IDF Vectorizer)
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# Lưu dữ liệu đã xử lý vào file (nếu cần sử dụng lại)
pd.DataFrame(X_train.toarray()).to_csv("X_train.csv", index=False)
pd.DataFrame(X_test.toarray()).to_csv("X_test.csv", index=False)
pd.DataFrame({"y_train": y_train}).to_csv("y_train.csv", index=False)
pd.DataFrame({"y_test": y_test}).to_csv("y_test.csv", index=False)

print("Hoàn thành tiền xử lý dữ liệu. File X_train.csv và y_train.csv đã sẵn sàng.")
