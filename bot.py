import os
import json
import urllib.request
import requests

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
PRODUCT_URL = "https://l.kaspi.kz/shop/HPqXuKbk822BST8"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({"chat_id": CHAT_ID, "text": text}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            print("Сообщение успешно отправлено!")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def check_kaspi_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(PRODUCT_URL, headers=headers, timeout=15)
        final_url = response.url
        print(f"Финальный URL товара: {final_url}")
        
        send_telegram_message(f"🔍 Бот проверяет товар по ссылке:\n{PRODUCT_URL}\nСтатус ответа Kaspi: {response.status_code}")
    except Exception as e:
        send_telegram_message(f"⚠️ Ошибка при запросе к Kaspi: {e}")

if __name__ == "__main__":
    check_kaspi_price()
