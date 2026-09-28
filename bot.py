import os
import json
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
PRODUCT_URL = "https://l.kaspi.kz/shop/HPqXuKbk822BST8"
MY_SHOP_KEYWORD = "dikhanbay"  # Ваш ключевой латинский идентификатор
MY_SHOP_DISPLAY_NAME = "ИП DIKHANBAY"

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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    try:
        response = requests.get(PRODUCT_URL, headers=headers, timeout=15)
        page_text = response.text
        
        # Ищем цены в тексте страницы
        prices = re.findall(r'"price"\s*:\s*(\d+)', page_text)
        valid_prices = [int(p) for p in prices if 100 < int(p) < 10000000]
        best_price = min(valid_prices) if valid_prices else None
        
        # Проверяем наличие вашего магазина во всем тексте (включая скрипты и JSON)
        my_shop_on_page = MY_SHOP_KEYWORD in page_text.lower()
        
        # Дополнительный поиск в скриптах (иногда данные продавцов лежат в JSON-массивах)
        if not my_shop_on_page:
            for script in BeautifulSoup(page_text, 'html.parser').find_all('script'):
                if script.string and MY_SHOP_KEYWORD in script.string.lower():
                    my_shop_on_page = True
                    break

        if best_price:
            status_icon = "Да ✅ (Вы на странице)" if my_shop_on_page else "Нет ❌ (Вас не видно в выдаче)"
            message = (
                f"🛡 Мониторинг позиции Kaspi:\n"
                f"📦 Товар: Крышка Stellox\n"
                f"💰 Лучшая цена на странице: {best_price} ₸\n"
                f"🏪 Статус магазина ({MY_SHOP_DISPLAY_NAME}): {status_icon}\n"
                f"🔗 {PRODUCT_URL}"
            )
            send_telegram_message(message)
        else:
            send_telegram_message(f"⚠️ Страница доступна, но цены не извлечены. Статус: {response.status_code}")
            
    except Exception as e:
        send_telegram_message(f"⚠️ Ошибка при запросе к Kaspi: {e}")

if __name__ == "__main__":
    check_kaspi_price()
