import os
import json
import urllib.request
import requests
from bs4 import BeautifulSoup

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
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    try:
        response = requests.get(PRODUCT_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        price = None
        
        # Способ 1: Ищем цену в JSON-LD разметке страницы
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    if data.get('@type') == 'Product' and 'offers' in data:
                        offers = data['offers']
                        if isinstance(offers, dict):
                            price = offers.get('price')
                        elif isinstance(offers, list) and len(offers) > 0:
                            price = offers[0].get('price')
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get('@type') == 'Product' and 'offers' in item:
                            offers = item['offers']
                            if isinstance(offers, dict):
                                price = offers.get('price')
            except Exception:
                pass
        
        # Способ 2: Запасной вариант (ищем текст с тенге, если микроразметка не отдала цену)
        if not price:
            for tag in soup.find_all(text=lambda t: t and '₸' in t):
                if len(tag.strip()) < 20:
                    price = tag.strip()
                    break

        if price:
            send_telegram_message(f"💰 Товар: Крышка расширительного бачка Stellox\nТекущая цена: {price} тенге\nСсылка: {PRODUCT_URL}")
        else:
            send_telegram_message(f"🔍 Страница доступна, но точную цену вытащить не удалось. Статус: {response.status_code}")
            
    except Exception as e:
        send_telegram_message(f"⚠️ Ошибка при парсинге Kaspi: {e}")

if __name__ == "__main__":
    check_kaspi_price()
