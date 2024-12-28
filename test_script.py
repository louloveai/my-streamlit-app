# Đoạn mã đầu tiên (25/12/2024)--------------------------------

import json
# --- Dữ liệu mẫu ---
training_data = {
    "vui": ["Tôi cảm thấy rất hạnh phúc!", "Hôm nay là một ngày tuyệt vời!", "Mọi thứ thật tốt đẹp!"],
    "buồn": ["Tôi không muốn làm gì cả.", "Cuộc sống thật tẻ nhạt.", "Tôi rất thất vọng."],
    "mệt mỏi": ["Tôi cần nghỉ ngơi.", "Tôi không có sức làm gì cả.", "Hôm nay thật kiệt sức."],
    "hạnh phúc": ["Tôi yêu cuộc sống này!", "Cảm giác này thật tuyệt vời.", "Tôi đang rất phấn khởi!"]
}

# --- Hàm phân loại cảm xúc ---
def detect_emotion(input_text):
    """Phân loại cảm xúc từ câu nhập vào."""
    for emotion, samples in training_data.items():
        for sample in samples:
            if sample.lower() in input_text.lower():
                return emotion
    return "Không xác định được cảm xúc."

# --- Hàm phân tích cảm xúc ---
def analyze_emotion():
    """Phân tích cảm xúc từ câu nhập."""
    user_input = input("Nhập câu của bạn để phân tích cảm xúc: ").strip()
    emotion = detect_emotion(user_input)
    print(f"Cảm xúc được nhận diện: {emotion}")

# --- Menu giao diện chính ---
def menu():
    """Menu chính."""
    menu_options = {
        "1": ("Phân tích cảm xúc từ câu nhập", analyze_emotion),
        "2": ("Thoát", None)
    }

    while True:
        print("\n==============================")
        print("----- Giao diện cảm xúc -----")
        print("==============================")
        for key, (desc, _) in menu_options.items():
            print(f"{key}. {desc}")

        choice = input("Nhập lựa chọn của bạn: ").strip()
        if choice in menu_options:
            action = menu_options[choice][1]
            if action:
                action()
            else:
                print("Hẹn gặp lại! Chúc bạn một ngày vui vẻ!")
                break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 2.")

# --- Chạy chương trình ---
if __name__ == "__main__":
    menu()

# Đoạn mã Training AI (26/12/2024)--------------------------------

import json

# Tệp JSON chứa dữ liệu training
TRAINING_FILE = "training_data.json"

# Tập dữ liệu cơ bản
training_data = [
    {"input": "Tôi rất vui hôm nay!", "label": "tích cực"},
    {"input": "Tôi buồn quá.", "label": "tiêu cực"},
    {"input": "Hôm nay là một ngày mệt mỏi.", "label": "tiêu cực"},
    {"input": "Cuộc sống thật hạnh phúc!", "label": "tích cực"},
    {"input": "Mọi thứ đều thất vọng.", "label": "tiêu cực"}
]

# Hàm lưu dữ liệu training vào file
def save_training_data(data, file_name=TRAINING_FILE):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Dữ liệu training đã được lưu vào {file_name}")

# Hàm training giả lập
def train_model(data):
    print("\n--- Bắt đầu Training ---")
    for entry in data:
        print(f"Training: {entry['input']} -> {entry['label']}")
    print("--- Training Hoàn Thành ---")

# Lưu dữ liệu training
save_training_data(training_data)

# Tiến hành training
train_model(training_data)

# Đoạn mã Dataset Training (27/12/2024)--------------------------------

import json

# Dataset mẫu cho training
training_data = [
    {"emotion": "vui", "response": "Thật tuyệt! Hãy chia sẻ niềm vui này với bạn bè hoặc làm điều gì bạn yêu thích."},
    {"emotion": "buồn", "response": "Hãy thử viết nhật ký hoặc tâm sự với một người bạn tin tưởng."},
    {"emotion": "thất vọng", "response": "Hãy thư giãn một chút hoặc tham gia hoạt động bạn yêu thích."},
    {"emotion": "mệt mỏi", "response": "Nghỉ ngơi với một tách trà ấm hoặc nghe nhạc thư giãn."},
    {"emotion": "hạnh phúc", "response": "Ghi lại khoảnh khắc này trong nhật ký hoặc chia sẻ niềm vui với gia đình."}
]

# Lưu dataset vào file JSON
def save_training_data(file_name="training_data.json"):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(training_data, file, ensure_ascii=False, indent=4)
    print("Dataset training đã được lưu vào file.")

# Load dataset từ file JSON
def load_training_data(file_name="training_data.json"):
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)

# Hàm training cơ bản (giả lập)
def train_emotion_model(data):
    print("\n--- Bắt đầu Training ---")
    for entry in data:
        print(f"Training với cảm xúc: {entry['emotion']}, phản hồi: {entry['response']}")
    print("Training hoàn tất!")

# Hàm kiểm tra mô hình sau khi training
def test_emotion_model():
    print("\n--- Kiểm tra mô hình ---")
    emotion_input = input("Nhập cảm xúc bạn muốn kiểm tra: ").strip().lower()
    response = next((item["response"] for item in training_data if item["emotion"] == emotion_input), None)
    if response:
        print(f"Phản hồi: {response}")
    else:
        print("Không tìm thấy phản hồi cho cảm xúc này.")

# Thực hiện training
save_training_data()
data = load_training_data()
train_emotion_model(data)
test_emotion_model()

# Đoạn mã nâng cao (28/12/2024) --------------------------------

import json

# Tên file chứa dữ liệu training
TRAINING_FILE = "training_data_advanced.json"

# Dữ liệu mẫu nâng cao cho training
training_data_advanced = [
    {"emotion": "vui", "response": "Hãy chia sẻ niềm vui này với ai đó hoặc tận hưởng khoảnh khắc của bạn!"},
    {"emotion": "buồn", "response": "Hãy thử ngồi thiền hoặc tâm sự với một người bạn thân thiết."},
    {"emotion": "thất vọng", "response": "Thư giãn bằng cách đi dạo hoặc nghe một podcast tích cực."},
    {"emotion": "mệt mỏi", "response": "Uống một cốc nước mát hoặc thử một bài tập yoga nhẹ nhàng."},
    {"emotion": "hạnh phúc", "response": "Ghi lại niềm vui này trong nhật ký và chia sẻ với người thân yêu!"}
]

# Lưu dữ liệu training nâng cao vào file JSON
def save_advanced_training_data(file_name=TRAINING_FILE):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(training_data_advanced, file, ensure_ascii=False, indent=4)
    print(f"Dữ liệu training nâng cao đã được lưu vào file '{file_name}'")

# Hàm load dữ liệu training nâng cao từ file JSON
def load_advanced_training_data(file_name=TRAINING_FILE):
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)

# Hàm giả lập quá trình training nâng cao
def advanced_train_model(data):
    print("\n--- Bắt đầu Training Nâng Cao ---")
    for entry in data:
        print(f"Training: '{entry['emotion']}' -> '{entry['response']}'")
    print("--- Training Nâng Cao Hoàn Thành ---")

# Hàm kiểm tra AI nâng cao sau khi training
def advanced_test_model():
    print("\n--- Kiểm tra mô hình nâng cao ---")
    emotion_input = input("Nhập cảm xúc bạn muốn kiểm tra: ").strip().lower()
    data = load_advanced_training_data()
    response = next((item["response"] for item in data if item["emotion"] == emotion_input), None)
    if response:
        print(f"Phản hồi AI: {response}")
    else:
        print("Không tìm thấy phản hồi cho cảm xúc này.")

# Chạy toàn bộ quy trình nâng cao
save_advanced_training_data()
data = load_advanced_training_data()
advanced_train_model(data)
advanced_test_model()

