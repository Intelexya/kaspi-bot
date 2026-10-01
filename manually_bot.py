import os
import json
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Список ваших товаров для сводного отчета
PRODUCTS = [
    {
        "name": "Крышка расширительного бачка Stellox",
        "url": "https://l.kaspi.kz/shop/HPqXuKbk822BST8",
        "my_price": 4010
    },
    {
        "name": "К2 крышка расширительного бачка 1647123010",
        "url": "https://kaspi.kz/shop/p/k2-kryshka-rasshiritelnogo-bachka-1647123010-154155028/?c=750000000",
        "my_price": 1800
    },
    {
        "name": "Japanparts крышка маслозаливной горловины K0016",
        "url": "https://kaspi.kz/shop/p/japanparts-kryshka-maslozalivnoi-gorloviny-ko016-165973425/?c=750000000",
        "my_price": 3315
    },
    {
        "name": "SRR крышка топливного бака 77300-33070",
        "url": "https://kaspi.kz/shop/p/srr-kryshka-toplivnogo-baka-77300-33070-116309998/?c=750000000",
        "my_price": 3492
    }
]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            print("Отчет успешно отправлен в Telegram!")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def generate_report():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    report_lines = ["📊 *Сводка по ценам на товары:*\n"]

    for index, item in enumerate(PRODUCTS, 1):
        print(f"Проверяем: {item['name']}...")
        try:
            response = requests.get(item['url'], headers=headers, timeout=15)
            page_text = response.text
            
            prices = re.findall(r'"price"\s*:\s*(\d+)', page_text)
            valid_prices = [int(p) for p in prices if 100 < int(p) < 10000000]
            best_price = min(valid_prices) if valid_prices else None
            
            if best_price:
                if best_price < item['my_price']:
                    status = f"❌ *Вы не первые!*\n   Низкая цена: {best_price} ₸ | Ваша: {item['my_price']} ₸"
                else:
                    status = f"✅ *Вы первые!*\n   Низкая цена: {best_price} ₸ | Ваша: {item['my_price']} ₸"
            else:
                status = "⚠️ Не удалось определить цену"
            
            report_lines.append(f"{index}️⃣ *{item['name']}*\n{status}\n")
        except Exception as e:
            report_lines.append(f"{index}️⃣ *{item['name']}*\n⚠️ Ошибка проверки\n")

    full_report = "\n".join(report_lines)
    send_telegram_message(full_report)

if __name__ == "__main__":
    generate_report()
