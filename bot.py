import os
import json
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    try:
        response = requests.get(PRODUCT_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        price = None
        
        # Способ 1: Ищем ключевые слова "price" в скрытых скриптах страницы
        matches = re.findall(r'"price"\s*:\s*(\d+)', response.text)
        if matches:
            for m in matches:
                val = int(m)
                # Фильтруем разумный диапазон цен для автозапчастей (от 100 до 10 000 000 тенге)
                if 100 < val < 10000000:
                    price = val
                    break
        
        # Способ 2: Если в скриптах не нашлось, ищем по классам ценовых блоков
        if not price:
            price_elems = soup.find_all(class_=re.compile("price", re.I))
            for elem in price_elems:
                txt = elem.get_text(strip=True)
                digits = "".join(filter(str.isdigit, txt))
                if digits and len(digits) <= 7:
                    price = digits
                    break

        if price:
            send_telegram_message(f"💰 Товар: Крышка расширительного бачка Stellox\nТекущая цена: {price} ₸\nСсылка: {PRODUCT_URL}")
        else:
            send_telegram_message(f"🔍 Страница доступна, но цена через регулярное выражение не поймана. Статус: {response.status_code}")
            
    except Exception as e:
        send_telegram_message(f"⚠️ Ошибка при парсинге Kaspi: {e}")

if __name__ == "__main__":
    check_kaspi_price()
