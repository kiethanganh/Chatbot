import json
import random
import re
from typing import Dict, List
import requests
import get_api



# Lưu trữ lịch sử trò chuyện
conversation_history: List[Dict[str, str]] = []

# Hàm tải cấu hình từ file JSON
def load_config(file_path: str = "intents.json") -> Dict:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return {}

# Hàm trích xuất tên thành phố
def extract_city(user_input: str) -> str:
    cities = ["hà nội", "tp hcm", "đà nẵng", "huế", "cần thơ", "nha trang", "new york"]
    user_input = user_input.lower()
    for city in cities:
        if city in user_input:
            return city.title()
    return "Hà Nội"

# Hàm trích xuất tên quốc gia
def extract_name(user_input: str) -> str:
    user_input = user_input.lower().strip()

    # Danh sách các cụm cần loại bỏ
    trash_words = ["quốc gia", "đất nước", "thông tin", "thông tin quốc gia", "thông tin đất nước", "về"]

    # Xóa các cụm từ gây nhiễu
    for word in trash_words:
        user_input = user_input.replace(word, "").strip()

    # Ánh xạ tên tiếng Việt sang tên API tiếng Anh
    country_map = {
        "việt nam": "vietnam",
        "tây ban nha": "spain",
        "thái lan": "thailand",
        "hoa kỳ": "united states",
        "mỹ": "united states",
        "nhật bản": "japan"
    }

    # Nếu người dùng không nhập gì cả
    if not user_input:
        return "Vui lòng nhập tên quốc gia (ví dụ: 'quốc gia Việt Nam')."

    return country_map.get(user_input, user_input)

# Hàm phát hiện ý định
def detect_intent(user_input: str, config: Dict) -> str:
    user_input = user_input.lower()

    weather_keywords = ["thời tiết", "dự báo thời tiết", "cho tôi biết thời tiết", "xem thời tiết"]
    country_keywords = ["quốc gia", "đất nước", "thông tin quốc gia", "thông tin đất nước"]

    # Check keywords bằng regex, tách từ ngữ để linh hoạt hơn
    for kw in country_keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', user_input):
            return "ask_country_info"

    for kw in weather_keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', user_input):
            return "ask_weather"

    if "tin tức" in user_input:
        return "ask_news"

    # Check cấu hình intents từ file JSON
    for intent, data in config.items():
        for keyword in data["keywords"]:
            if re.search(r'\b' + re.escape(keyword) + r'\b', user_input):
                return intent

    return None

# Hàm xử lý phản hồi
last_intent = None  # đặt ở đầu file hoặc global

def chatbot_response(user_input: str) -> str:
    global conversation_history

    if not user_input or user_input.strip() == "":
        return "Bạn chưa nhập gì cả, hãy thử nói gì đó nhé!"

    user_input = user_input.strip()
    config = load_config("intents.json")
    intent = detect_intent(user_input, config)
    
    conversation_history.append({"input": user_input, "intent": intent})

    # === Các keyword ===
    weather_keywords = config.get("ask_weather", {}).get("keywords", [])
    country_keywords = config.get("ask_country_info", {}).get("keywords", [])

    # === Thành phố hỗ trợ ===
    supported_cities = ["Hà Nội", "TP HCM", "Đà Nẵng", "Huế", "Cần Thơ", "Nha Trang", "New York"]

    # === 1. Gợi ý THỜI TIẾT nếu chưa rõ thành phố ===
    if intent == "ask_weather" or any(kw in user_input.lower() for kw in weather_keywords):
        if not any(city.lower() in user_input.lower() for city in supported_cities):
            return (
                "🌤️ Tôi có thể cung cấp thời tiết cho các thành phố: "
                + ", ".join(supported_cities)
                + "<br>Bạn hãy nhập lại với tên thành phố cụ thể nhé!"
            )
        else:
            city = extract_city(user_input)
            response = get_api.get_weather(city)

    # === 2. Gợi ý QUỐC GIA nếu chưa rõ tên ===
    elif intent == "ask_country_info" or any(kw in user_input.lower() for kw in country_keywords):
        name = extract_name(user_input)
        if name == "Vui lòng nhập tên quốc gia (ví dụ: 'quốc gia Việt Nam').":
            return (
                "🌍 Bạn muốn biết thông tin quốc gia nào?<br>"
            "Hãy nhập như sau: <b>quốc gia Việt Nam</b>, <b>quốc gia Tây Ban Nha</b>, v.v.<br>"
            "Hoặc bạn có thể tìm kiếm bất kỳ quốc gia nào: quốc gia + Country English Name. Vd: quốc gia singapore"
            )
        response = get_api.get_country_info(name)

    # === 3. Lấy tin tức ===
    elif intent == "ask_news":
        response = get_api.get_news()

    # === 4. Các phản hồi thông thường từ file intents.json ===
    elif intent and intent in config:
        response = random.choice(config[intent]["responses"])
        response = response.replace('\n', '<br>') 

    else:
        response = "Tôi không hiểu, bạn có thể hỏi lại không?"

    conversation_history.append({"input": response, "intent": "bot_response"})
    return response

def reset_conversation():
    global conversation_history
    conversation_history = []

def get_conversation_history():
    return conversation_history




