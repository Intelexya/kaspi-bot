import os
import json
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
PRODUCT_URL = "https://l.kaspi.kz/shop/HPqXuKbk822BST8"

# Укажите вашу текущую цену на этот товар. 
# Если кто-то на рынке поставит цену ниже этой — бот пришлет предупреждение.
MY_PRICE = 4010 

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
        
        # Ищем все цены на странице
        prices = re.findall(r'"price"\s*:\s*(\d+)', page_text)
        valid_prices = [int(p) for p in prices if 100 < int(p) < 10000000]
        best_price = min(valid_prices) if valid_prices else None
        
        if best_price:
            print(f"Найдена минимальная цена на рынке: {best_price} ₸")
            # Если минимальная цена конкурентов ниже вашей цены
            if best_price < MY_PRICE:
                message = (
                    f"🚨 **Внимание! Появилась цена ниже вашей!**\n"
                    f"📦 Товар: Крышка Stellox\n"
                    f"💰 Лучшая цена на рынке: {best_price} ₸\n"
                    f"🏷 Ваша установленная цена: {MY_PRICE} ₸\n"
                    f"🔗 {PRODUCT_URL}"
                )
                send_telegram_message(message)
            else:
                print(f"Всё отлично! Лучшая цена ({best_price} ₸) не ниже вашей ({MY_PRICE} ₸). Уведомление не требуется.")
        else:
            print("Страница доступна, но цены не извлечены.")
            
    except Exception as e:
        send_telegram_message(f"⚠️ Ошибка при запросе к Kaspi: {e}")

if __name__ == "__main__":
    check_kaspi_price()
