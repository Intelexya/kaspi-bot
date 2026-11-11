import os
import json
import urllib.request
import requests
import re
import time
import random

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Автоматически загружаем список товаров из файла products.json
try:
    with open('products.json', 'r', encoding='utf-8') as f:
        PRODUCTS = json.load(f)
    print(f"Успешно загружено товаров из файла: {len(PRODUCTS)}")
except Exception as e:
    print(f"Ошибка при чтении products.json: {e}")
    PRODUCTS = []

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({"chat_id": CHAT_ID, "text": text}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            print("Сообщение успешно отправлено в Telegram!")
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

def generate_report():
    if not PRODUCTS:
        print("Список товаров пуст!")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    print(f"Всего товаров для проверки: {len(PRODUCTS)}")
    report_items = []

    for index, item in enumerate(PRODUCTS, 1):
        print(f"Проверяем [{index}/{len(PRODUCTS)}]: {item['name']}...")
    
        # Защита на случай, если в JSON у какого-то товара нет ключа 'my_price' или 'url'
        item_price = item.get('my_price', 0)
        item_url = item.get('url', '')
        item_name = item.get('name', 'Товар без названия')

        if not item_url:
            report_items.append(f"{index}. {item_name}\n⚠️ Ошибка: нет ссылки\n")
            continue

        try:
            response = requests.get(item_url, headers=headers, timeout=15)
            page_text = response.text

            prices = re.findall(r'"price"\s*:\s*(\d+)', page_text)
            valid_prices = [int(p) for p in prices if 100 < int(p) < 10000000]
            best_price = min(valid_prices) if valid_prices else None

            if best_price:
                if best_price < item_price:
                    status = f"❌ Вы не первый!\n   Низкая цена: {best_price} ₸ | Ваша: {item_price} ₸"
                else:
                    status = f"✅ Вы первый!\n   Низкая цена: {best_price} ₸ | Ваша: {item_price} ₸"
            else:
                status = "⚠️ Не удалось определить цену"

            report_items.append(f"{index}. {item_name}\n{status}\n")
        except Exception as e:
            report_items.append(f"{index}. {item_name}\n⚠️ Ошибка проверки\n")

        # Случайная пауза между товарами
        time.sleep(random.uniform(2.0, 4.0))

    # Делим весь список на части по 15 товаров, чтобы каждое сообщение гарантированно влезало в лимит Telegram (4096 символов)
    chunk_size = 15
    chunks = [report_items[i:i + chunk_size] for i in range(0, len(report_items), chunk_size)]

    # Отправляем заголовок
    send_telegram_message(f"📊 Сводка по ценам на автозапчасти (всего товаров: {len(PRODUCTS)}):")
    time.sleep(1)

    # Отправляем каждую часть с паузой в 1 секунду
    for i, chunk in enumerate(chunks, 1):
        chunk_text = f"--- Часть {i} из {len(chunks)} ---\n\n" + "\n".join(chunk)
        send_telegram_message(chunk_text)
        time.sleep(1)

if __name__ == "__main__":
    generate_report()