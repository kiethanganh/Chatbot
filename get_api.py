import requests
from datetime import datetime
import pytz
import feedparser

def get_news() -> str:
    feed_url = "https://news.google.com/rss?hl=vi&gl=VN&ceid=VN:vi"
    try:
        feed = feedparser.parse(feed_url)
        if feed.entries:
            news_jsx = [
                f'''
                <div style="margin-bottom: 1em;">
                    <a href="{entry.link}" target="_blank" rel="noopener noreferrer"
                       style="color: white; text-decoration: none;">
                        {entry.title}
                    </a><br/>
                    <small><i>{entry.published}</i></small>
                </div>
                '''.strip()
                for entry in feed.entries[:5]
            ]
            return "\n".join(news_jsx)
        return "<p>Không tìm thấy tin tức từ Google News.</p>"
    except Exception as e:
        return f'<p>Lỗi khi lấy tin tức: {str(e)}</p>'

# API key từ OpenWeather do bạn cung cấp
API_KEY = "c27fefacf9b9e98ae7c8e6615a4875ca"

def get_weather(city: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=vi&units=metric"

    try:
        response = requests.get(url).json()
        if response.get("cod") == 200:
            weather = response["weather"][0]["description"]
            temp = response["main"]["temp"]
            feels_like = response["main"]["feels_like"]
            humidity = response["main"]["humidity"]
            wind_speed = response["wind"]["speed"]
            
            vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
            current_time = datetime.now(vn_timezone).strftime('%H:%M %d/%m/%Y')

            html_output = f"""
            <div class="botText" style="background-color: #1e1e2f; padding: 1em; border-radius: 10px; color: white; font-family: Arial;">
            <h3 style="margin-top: 0;">🌤️ Thời tiết ở <strong>{city.title()}</strong> lúc {current_time}</h3>
            <p>🌡️ Nhiệt độ: <strong>{temp:.1f}°C</strong> (Cảm giác như <strong>{feels_like:.1f}°C</strong>)</p>
            <p>💧 Độ ẩm: <strong>{humidity}%</strong></p>
            <p>🌬️ Gió: <strong>{wind_speed} m/s</strong></p>
            <p>📝 Mô tả: <em>{weather}</em></p>
        </div>
        """.strip()
            return html_output

        return f"Lỗi API: {response.get('message', 'Không tìm thấy thông tin thời tiết.')}"

    except requests.RequestException as e:
        return f"Lỗi kết nối: {str(e)}"

    
# Hàm lấy thông tin quốc gia
def get_country_info(name: str) -> str:
    if name == "Vui lòng nhập tên quốc gia (ví dụ: 'quốc gia Việt Nam').":
        return f'<p>{name}</p>'

    try:
        url = f"https://restcountries.com/v3.1/name/{name}"
        response = requests.get(url, timeout=5).json()

        if response and "status" not in response:
            country = response[0]

            common_name = country['name'].get('common', 'Không rõ')
            official_name = country['name'].get('official', 'Không rõ')
            capital = country.get('capital', ['Không rõ'])[0]
            region = country.get('region', 'Không rõ')
            population = f"{country.get('population', 0):,}"

            return f'''
                <div style="margin: 1em 0; padding: 1em; border-left: 6px solid #1e90ff;
                            background: rgba(30, 144, 255, 0.1); border-radius: 10px;">
                    <strong>🌍 Quốc gia:</strong> {common_name}<br/>
                    <strong>📜 Tên chính thức:</strong> {official_name}<br/>
                    <strong>🏛️ Thủ đô:</strong> {capital}<br/>
                    <strong>🌐 Khu vực:</strong> {region}<br/>
                    <strong>👥 Dân số:</strong> {population} người<br/>
                </div>
            '''.strip()

        return f'<p>Không tìm thấy thông tin về quốc gia "{name}". Hãy thử tên tiếng Anh như "Spain" thay vì "Tây Ban Nha".</p>'

    except requests.RequestException as e:
        return f'<p>Lỗi khi lấy thông tin quốc gia: {str(e)}</p>'
    
    # Hàm lấy tin tức từ Google News RSS
def get_news() -> str:
    feed_url = "https://news.google.com/rss?hl=vi&gl=VN&ceid=VN:vi"
    try:
        feed = feedparser.parse(feed_url)
        if feed.entries:
            news_jsx = [
                f'''
                <div style="margin-bottom: 1em;">
                    <a href="{entry.link}" target="_blank" rel="noopener noreferrer"
                       style="color: white; text-decoration: none;">
                        {entry.title}
                    </a><br/>
                    <small><i>{entry.published}</i></small>
                </div>
                '''.strip()
                for entry in feed.entries[:5]
            ]
            return "\n".join(news_jsx)
        return "<p>Không tìm thấy tin tức từ Google News.</p>"
    except Exception as e:
        return f'<p>Lỗi khi lấy tin tức: {str(e)}</p>'
