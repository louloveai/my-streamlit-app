import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Đọc dữ liệu huấn luyện và kiểm tra
X_train = pd.read_csv("X_train.csv")
X_test = pd.read_csv("X_test.csv")
y_train = pd.read_csv("y_train.csv")["y_train"]
y_test = pd.read_csv("y_test.csv")["y_test"]

# Huấn luyện mô hình Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = model.predict(X_test)

# Đánh giá độ chính xác
accuracy = accuracy_score(y_test, y_pred)
print(f"Độ chính xác của mô hình: {accuracy * 100:.2f}%")

# Lưu mô hình đã huấn luyện
joblib.dump(model, "chatbot_model.pkl")
print("Mô hình đã được lưu vào chatbot_model.pkl")

# Ví dụ thêm dữ liệu
additional_data = "path_to_new_cleaned_data.json"
with open(additional_data, 'r', encoding='utf-8') as file:
    new_data = json.load(file)
dataset.extend(new_data)
