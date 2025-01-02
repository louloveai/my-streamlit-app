from googletrans import Translator
from transformers import pipeline
import pandas as pd

def process_data(input_file, output_file):
    # Đọc dữ liệu
    data = pd.read_csv(input_file)

    # Lọc dữ liệu
    keywords = ["stress", "healing", "anxiety", "mental health", "calm", "relaxation"]
    data = data[data['content'].str.contains('|'.join(keywords), case=False, na=False)]

    # Dịch nội dung
    translator = Translator()
    data['content_vi'] = data['content'].apply(lambda x: translator.translate(x, src='en', dest='vi').text)

    # Tóm tắt nội dung
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    data['summary'] = data['content_vi'].apply(lambda x: summarizer(x, max_length=150, min_length=50, do_sample=False)[0]['summary_text'])

    # Lưu kết quả
    data.to_csv(output_file, index=False)
    print(f"Dữ liệu xử lý xong lưu tại {output_file}")

# Ví dụ gọi hàm xử lý
if __name__ == "__main__":
    process_data("input_data.csv", "final_data.csv")
