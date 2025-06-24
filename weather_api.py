import requests
from datetime import datetime
import pytz

# API key từ OpenWeather do bạn cung cấp
API_KEY = "c27fefacf9b9e98ae7c8e6615a4875ca"

def get_weather(city: str) -> str:
    """
    Lấy thông tin thời tiết từ OpenWeatherMap dựa trên tên thành phố.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=vi&units=metric"
    
    try:
        response = requests.get(url).json()
        print(f"API Response: {response}")  # Thêm log để debug
        if response.get("cod") == 200:
            weather = response["weather"][0]["description"]
            temp = response["main"]["temp"]
            vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
            current_time = datetime.now(vn_timezone).strftime('%H:%M %d/%m/%Y')
            return f"Thời tiết ở {city} lúc {current_time} là {weather}, nhiệt độ {temp:.1f}°C."
        return f"Lỗi API: {response.get('message', 'Không tìm thấy thông tin thời tiết cho {city}')}"
    except requests.RequestException as e:
        return f"Lỗi kết nối: {str(e)}"