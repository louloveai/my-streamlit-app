import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import os
import json
from googletrans import Translator

# ====== Đọc dữ liệu từ file CSV ======
def load_data(file_path):
    """
    Đọc dữ liệu từ file CSV và trả về DataFrame
    """
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"File {file_path} không tồn tại.")

# ====== Dịch dữ liệu (nếu cần thiết) ======
def translate_texts(texts, target_language="vi"):
    """
    Dịch danh sách các đoạn văn bản sang ngôn ngữ đích
    """
    translator = Translator()
    translated_texts = []
    for text in texts:
        try:
            translated = translator.translate(text, dest=target_language).text
            translated_texts.append(translated)
        except Exception as e:
            print(f"Không thể dịch: {text}. Lỗi: {e}")
            translated_texts.append(text)  # Giữ nguyên nếu dịch thất bại
    return translated_texts

# ====== Làm sạch dữ liệu ======
def clean_data(df):
    """
    Loại bỏ các dòng trống và trùng lặp
    """
    df = df.dropna(subset=["message"])
    df = df.drop_duplicates(subset=["message"])
    return df

# ====== Tách dữ liệu thành input và output ======
def split_features_and_labels(df):
    """
    Tách dữ liệu thành X (input) và y (label)
    """
    X = df["message"]
    y = df["label"]
    return X, y

# ====== Vector hóa văn bản ======
def vectorize_text(X):
    """
    Vector hóa dữ liệu văn bản bằng TF-IDF
    """
    vectorizer = TfidfVectorizer(max_features=5000)
    X_vectorized = vectorizer.fit_transform(X)
    return X_vectorized, vectorizer

# ====== Chia dữ liệu thành tập huấn luyện và kiểm tra ======
def split_train_test(X, y, test_size=0.2, random_state=42):
    """
    Chia dữ liệu thành tập train và test
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

# ====== Lưu dữ liệu đã xử lý ======
def save_processed_data(X_train, X_test, y_train, y_test, output_dir="processed_data"):
    """
    Lưu dữ liệu đã xử lý vào các file CSV
    """
    os.makedirs(output_dir, exist_ok=True)
    pd.DataFrame(X_train).to_csv(os.path.join(output_dir, "X_train.csv"), index=False)
    pd.DataFrame(X_test).to_csv(os.path.join(output_dir, "X_test.csv"), index=False)
    pd.DataFrame(y_train).to_csv(os.path.join(output_dir, "y_train.csv"), index=False)
    pd.DataFrame(y_test).to_csv(os.path.join(output_dir, "y_test.csv"), index=False)

# ====== Chạy các bước xử lý ======
if __name__ == "__main__":
    # Bước 1: Đọc dữ liệu
    file_path = "chat_history.csv"
    try:
        data = load_data(file_path)
    except FileNotFoundError as e:
        print(e)
        exit()

    # Bước 2: Dịch dữ liệu sang tiếng Việt
    data["message"] = translate_texts(data["message"].tolist())

    # Bước 3: Làm sạch dữ liệu
    data = clean_data(data)

    # Bước 4: Tách X và y
    X, y = split_features_and_labels(data)

    # Bước 5: Vector hóa dữ liệu
    X_vectorized, vectorizer = vectorize_text(X)

    # Bước 6: Chia tập train và test
    X_train, X_test, y_train, y_test = split_train_test(X_vectorized, y)

    # Bước 7: Lưu dữ liệu đã xử lý
    save_processed_data(X_train, X_test, y_train, y_test)

    print("Xử lý dữ liệu hoàn tất và đã lưu vào thư mục 'processed_data'.")
