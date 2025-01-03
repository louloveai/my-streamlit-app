import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        soup = BeautifulSoup(response.content, 'lxml')

        # Lấy tiêu đề bài viết
        title = soup.find('title').text if soup.find('title') else "No Title"

        # Lấy nội dung bài viết
        paragraphs = soup.find_all('p')
        content = '\n'.join([para.text for para in paragraphs])

        return {
            "title": title,
            "content": content
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def save_to_file(data, output_path="scraped_data.json"):
    import json
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {output_path}")

# Ví dụ URL và cách sử dụng
if __name__ == "__main__":
    urls = [
        "https://wellcare.vn/tam-ly-than-kinh/7-cach-chua-lanh-vet-thuong-tam-ly",
        "https://thanhnien.vn/chua-lanh-la-gi-va-vi-sao-nguoi-ta-thich-di-chua-lanh-185240515144931615.htm"
        "https://dienmaycholon.com/kinh-nghiem-mua-sam/chua-lanh-la-gi-tai-sao-moi-nguoi-hay-ru-nhau-di-chua-lanh"
        "https://cand.com.vn/nguoi-trong-cuoc/trao-luu-chua-lanh-co-thuc-su-chua-lanh--i713460/"
        "https://nhathuoclongchau.com.vn/bai-viet/healing-la-gi-hieu-dung-ve-healing-de-chua-lanh-hieu-qua.html"
        "https://nhathuoclongchau.com.vn/bai-viet/hoc-cach-chua-lanh-vet-thuong-tam-ly.html"
        "https://www.vinmec.com/vie/bai-viet/cach-chua-lanh-vet-thuong-sau-bien-co-vi"
        "https://caodangyhanoi.org/chua-lanh-tam-hon-co-kho-khong-lam-sao-de-chua-lanh-tam-hon/"
        "https://www.himalaya-vn.com/blogs/tin-tuc/can-lam-gi-de-bat-dau-hanh-trinh-tu-chua-lanh-cho-chinh-minh?srsltid=AfmBOoqfHzLClMYB9GV-Rj9Qj4-wk8v3DPOorLWO3bGHH23U3EDyuLJc"
        "https://9soul.vn/blog/10-cach-tu-chua-lanh-tam-hon-tai-nha
    ]

    all_data = []
    for url in urls:
        scraped_data = scrape_article(url)
        if scraped_data:
            all_data.append(scraped_data)

    save_to_file(all_data)
