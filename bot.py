import os
import json
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
PRODUCT_URL = "https://l.kaspi.kz/shop/HPqXuKbk822BST8"
MY_SHOP_NAME = "ИП DIKHANBAY"

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
        
        page_text = response.text
        
        # Ищем минимальную цену на странице
        prices = re.findall(r'"price"\s*:\s*(\d+)', page_text)
        valid_prices = [int(p) for p in prices if 100 < int(p) < 10000000]
        best_price = min(valid_prices) if valid_prices else None
        
        # Проверяем, упоминается ли наш магазин на странице вообще
        my_shop_on_page = MY_SHOP_NAME.lower() in page_text.lower()
        
        # Проверим, кто стоит выше (в коде первый попавшийся продавец или анализ позиций)
        # Если наш магазин на странице есть, но минимальная цена принадлежит кому-то другому
        if best_price:
            # Для точной проверки: если наш магазин не на первом месте или цена конкурента ниже
            # Отправим отчет о текущей ситуации
            message = (
                f"🛡 Мониторинг позиции Kaspi:\n"
                f"📦 Товар: Крышка Stellox\n"
                f"💰 Лучшая цена на странице: {best_price} ₸\n"
                f"🏪 Ваш магазин ({MY_SHOP_NAME}) присутствует: {'Да ✅' if my_shop_on_page else 'Нет ❌'}\n"
                f"🔗 {PRODUCT_URL}"
            )
            send_telegram_message(message)
        else:
            send_telegram_message(f"⚠️ Страница доступна, но цены не удалось извлечь. Статус: {response.status_code}")
            
    except Exception as e:
        send_telegram_message(f"⚠️ Ошибка при запросе к Kaspi: {e}")

if __name__ == "__main__":
    check_kaspi_price()
