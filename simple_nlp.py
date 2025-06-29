import json
import random
import re
from typing import Dict, List
import requests
import weather_api
import feedparser

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
    country_map = {"việt nam": "vietnam", "tây ban nha": "spain", "thái lan": "thailand"}
    if "quốc gia" in user_input:
        name = user_input.replace("quốc gia", "").strip()
        if not name:
            return "Vui lòng nhập tên quốc gia (ví dụ: 'quốc gia Việt Nam')."
    else:
        name = user_input
    return country_map.get(name, name)

# Hàm lấy thông tin quốc gia
def get_country_info(name: str) -> str:
    if name == "Vui lòng nhập tên quốc gia (ví dụ: 'quốc gia Việt Nam').":
        return name
    try:
        url = f"https://restcountries.com/v3.1/name/{name}"
        response = requests.get(url, timeout=5).json()
        if response and "status" not in response:
            country = response[0]
            return f"Thông tin về {country['name']['common']}: Thủ đô {country['capital'][0]}, dân số {country['population']:,}, khu vực {country['region']}."
        return f"Không tìm thấy thông tin về quốc gia {name} (thử tên chuẩn như 'Spain' thay vì 'Tây Ban Nha')."
    except requests.RequestException as e:
        return f"Lỗi khi lấy thông tin quốc gia: {str(e)}."

# Hàm lấy tin tức từ Google News RSS
def get_news() -> str:
    feed_url = "https://news.google.com/rss?hl=vi&gl=VN&ceid=VN:vi"
    try:
        feed = feedparser.parse(feed_url)
        if feed.entries:
            news = [f"{entry.title} - {entry.link}" for entry in feed.entries[:5]]  # Lấy 5 tin đầu
            return "\n".join(news)
        return "Không tìm thấy tin tức từ Google News."
    except Exception as e:
        return f"Lỗi khi lấy tin tức: {str(e)}."

# Hàm phát hiện ý định
def detect_intent(user_input: str, config: Dict) -> str:
    user_input = user_input.lower()
    if "quốc gia" in user_input:
        return "ask_country_info"
    elif "tin tức" in user_input:
        return "ask_news"
    for intent, data in config.items():
        for keyword in data["keywords"]:
            if re.search(r'\b' + re.escape(keyword) + r'\b', user_input):
                return intent
    return None

# Hàm xử lý phản hồi
def chatbot_response(user_input: str) -> str:
    global conversation_history
    
    if not user_input or user_input.strip() == "":
        response = "Bạn chưa nhập gì cả, hãy thử nói gì đó nhé!"
    else:
        user_input = user_input.strip()
        config = load_config("intents.json")
        intent = detect_intent(user_input, config)
        
        conversation_history.append({"input": user_input, "intent": intent})
        
        if intent == "ask_country_info":
            name = extract_name(user_input)
            response = get_country_info(name)
        elif intent == "ask_weather":
            if len(conversation_history) > 1 and conversation_history[-2]["intent"] == "ask_weather":
                city = extract_city(user_input)
                response = weather_api.get_weather(city)
            else:
                city = extract_city(user_input)
                response = weather_api.get_weather(city)
        elif intent == "ask_news":
            response = get_news()
        elif intent and intent in config:
            response = random.choice(config[intent]["responses"])
        else:
            response = "Tôi không hiểu, bạn có thể hỏi lại không?"
    
    conversation_history.append({"input": response, "intent": "bot_response"})
    return response

def reset_conversation():
    global conversation_history
    conversation_history = []

def get_conversation_history():
    return conversation_history
