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
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    try:
        response = requests.get(PRODUCT_URL, headers=headers, timeout=15)
        print(f"Финальный URL: {response.url}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем цену на странице Kaspi (пробуем разные варианты блоков цены)
        price_text = None
        
        # Вариант 1: Поиск по структуре данных или классам цены
        price_elem = soup.find(class_=re.compile("item__price|price", re.I))
        if price_elem:
            price_text = price_elem.get_text(strip=True)
        
        if price_text:
            send_telegram_message(f"💰 Товар: Крышка Stellox\nТекущая цена: {price_text}\nСсылка: {PRODUCT_URL}")
        else:
            # Если точный класс не нашли, отправим уведомление, что страница открылась, но структура изменилась
            send_telegram_message(f"🔍 Страница доступна, но цена не найдена автоматически. Статус: {response.status_code}")
            
    except Exception as e:
        send_telegram_message(f"⚠️ Ошибка при парсинге Kaspi: {e}")

if __name__ == "__main__":
    check_kaspi_price()
