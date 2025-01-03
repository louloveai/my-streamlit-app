import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import os
import json
from googletrans import Translator
import requests
from bs4 import BeautifulSoup

# Thêm mã để scrape nội dung từ các trang báo vào file
def fetch_article_content(url):
    """
    Lấy nội dung chính của một bài báo từ URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Ví dụ: Lấy nội dung từ thẻ <p>, tùy chỉnh theo cấu trúc trang báo.
        paragraphs = soup.find_all('p')
        content = "\n".join([p.get_text() for p in paragraphs])
        
        # Lọc bỏ nội dung quá ngắn hoặc không cần thiết.
        if len(content) > 100:  # Chỉ lấy bài viết dài hơn 100 ký tự.
            return content
        else:
            return None
    except Exception as e:
        print(f"Lỗi khi lấy nội dung từ {url}: {e}")
        return None

# Thêm hàm xử lý danh sách URL để scrape nội dung hàng loạt.
def scrape_articles_from_urls(url_list, output_file="articles.txt"):
    """
    Scrape nội dung từ danh sách URL và lưu vào file.
    """
    all_content = []
    for url in url_list:
        print(f"Đang xử lý: {url}")
        content = fetch_article_content(url)
        if content:
            all_content.append(content)
        else:
            print(f"Nội dung từ {url} không phù hợp hoặc không tải được.")

    # Lưu nội dung vào file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n\n".join(all_content))
    print(f"Đã lưu nội dung vào file: {output_file}")

# ====== Đọc dữ liệu từ file CSV ======
def load_data(file_path):
    """
    Đọc dữ liệu từ file CSV và trả về DataFrame
    """
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"File {file_path} không tồn tại.")

# Khởi tạo mô hình tóm tắt và viết lại nội dung
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
rewriter = pipeline("text2text-generation", model="t5-small")

def clean_article(article):
    """
    Lọc bỏ các phần không cần thiết trong bài báo.
    """
    # Loại bỏ quảng cáo, HTML, và dòng trống
    article = re.sub(r'<[^>]+>', '', article)  # Xóa HTML tags
    article = re.sub(r'Advertisement|Quảng cáo', '', article)
    article = re.sub(r'\s+', ' ', article).strip()
    return article

def process_article(article):
    """
    Tóm tắt và viết lại nội dung bài báo.
    """
    # Tóm tắt nội dung
    summarized = summarizer(article, max_length=150, min_length=50, do_sample=False)
    summary = summarized[0]['summary_text']

    # Viết lại nội dung
    rewritten = rewriter(summary)
    return rewritten[0]['generated_text']

def process_articles(directory, output_directory):
    """
    Đọc bài báo từ thư mục, xử lý, và lưu kết quả vào thư mục output.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                article = file.read()
            cleaned = clean_article(article)
            processed = process_article(cleaned)

            # Lưu bài báo đã xử lý
            output_file = os.path.join(output_directory, filename)
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(processed)
            print(f"Đã xử lý: {filename}")

if __name__ == "__main__":
    input_dir = "articles_raw"
    output_dir = "processed_articles"
    os.makedirs(output_dir, exist_ok=True)
    process_articles(input_dir, output_dir)

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
def preprocess_articles(input_file, output_file):
    """
    Tiền xử lý nội dung từ file input và lưu kết quả vào file output.
    Các bước tiền xử lý:
    - Loại bỏ các quảng cáo, nội dung không liên quan.
    - Chuẩn hóa văn bản: xóa ký tự thừa, viết thường, và loại bỏ dấu câu nếu cần.
    """
    with open(input_file, "r", encoding="utf-8") as infile:
        raw_text = infile.readlines()

    processed_lines = []
    for line in raw_text:
        # Bỏ qua các dòng quá ngắn (quảng cáo hoặc không liên quan)
        if len(line.strip()) > 30:
            # Xóa các ký tự đặc biệt, giữ lại từ ngữ
            cleaned_line = re.sub(r"[^a-zA-Z0-9À-ỹ\s]", "", line.strip())
            processed_lines.append(cleaned_line.lower())

    # Lưu kết quả sau khi tiền xử lý
    with open(output_file, "w", encoding="utf-8") as outfile:
        for line in processed_lines:
            outfile.write(line + "\n")

if __name__ == "__main__":
    # Gọi hàm tiền xử lý
    preprocess_articles(input_file="articles.txt", output_file="processed_articles.txt")

