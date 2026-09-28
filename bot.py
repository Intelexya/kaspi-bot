import os
import json
import urllib.request
import requests
from bs4 import BeautifulSoup
import re

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Список ваших товаров для мониторинга
# Вы можете легко добавлять сюда новые запчасти по аналогии
PRODUCTS = [
    {
        "name": "Крышка расширительного бачка Stellox",
        "url": "https://l.kaspi.kz/shop/HPqXuKbk822BST8",
        "my_price": 4010
    },
    # Пример второго товара (когда собредитесь добавить, просто раскомментируйте и заполните):
     {
         "name": "K2 крышка расширительного бачка 1647123010",
         "url": "https://kaspi.kz/shop/p/k2-kryshka-rasshiritel-nogo-bachka-1647123010-154155028/?c=750000000",
         "my_price": 1800
     }

     {
         "name": "Japanparts крышка маслозаливной горловины KO016",
         "url": "https://kaspi.kz/shop/p/japanparts-kryshka-maslozalivnoi-gorloviny-ko016-165973425/?c=750000000",
         "my_price": 3315
     }
    
     {
         "name": "SRR крышка топливного бака 77300-33070",
         "url": "https://kaspi.kz/shop/p/srr-kryshka-toplivnogo-baka-77300-33070-116309998/?c=750000000",
         "my_price": 3492
     }


     {
         "name": "Longho крышка омывателя 9650135",
         "url": "https://kaspi.kz/shop/p/longho-kryshka-omyvatelja-9650135-167733700/?c=750000000",
         "my_price": 1498
     }

     {
         "name": "Крышка топливного бака 7730006040",
         "url": "https://kaspi.kz/shop/p/kryshka-toplivnogo-baka-7730006040-154439341/?c=750000000",
         "my_price": 5700
     }

     {
         "name": "Stellox крышка расширительного бачка 7550961SX",
         "url": "https://kaspi.kz/shop/p/stellox-kryshka-rasshiritel-nogo-bachka-7550961sx-129853133/?c=750000000",
         "my_price": 2997
     }

     {
         "name": "WXQP крючок солнцезащитного козырька 199157559",
         "url": "https://kaspi.kz/shop/p/wxqp-krjuchok-solntsezaschitnogo-kozyr-ka-199157559-164727533/?c=750000000",
         "my_price": 1300
     }

     {
         "name": "JP GROUP крышка омывателя 1198600300 Audi A1",
         "url": "https://kaspi.kz/shop/p/jp-group-kryshka-omyvatelja-1198600300-audi-a1-129686813/?c=750000000",
         "my_price": 1790
     }

     {
         "name": "DEKO крышка омывателя D85316-26030",
         "url": "https://kaspi.kz/shop/p/deko-kryshka-omyvatelja-d85316-26030-168231986/?c=750000000",
         "my_price": 2010
     }

     {
         "name": "K2 крючок солнцезащитного козырька 3B0857561B",
         "url": "https://kaspi.kz/shop/p/k2-krjuchok-solntsezaschitnogo-kozyr-ka-3b0857561b-166974655/?c=750000000",
         "my_price": 2000
     }

]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({"chat_id": CHAT_ID, "text": text}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            print("Сообщение успешно отправлено!")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def check_kaspi_prices():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }

    for item in PRODUCTS:
        print(f"Проверяем товар: {item['name']}...")
        try:
            response = requests.get(item['url'], headers=headers, timeout=15)
            page_text = response.text
            
            prices = re.findall(r'"price"\s*:\s*(\d+)', page_text)
            valid_prices = [int(p) for p in prices if 100 < int(p) < 10000000]
            best_price = min(valid_prices) if valid_prices else None
            
            if best_price:
                print(f"Лучшая цена на рынке: {best_price} ₸ (Ваша: {item['my_price']} ₸)")
                if best_price < item['my_price']:
                    message = (
                        f"🚨 **Внимание! Появилась цена ниже вашей!**\n"
                        f"📦 Товар: {item['name']}\n"
                        f"💰 Лучшая цена на рынке: {best_price} ₸\n"
                        f"🏷 Ваша установленная цена: {item['my_price']} ₸\n"
                        f"🔗 {item['url']}"
                    )
                    send_telegram_message(message)
            else:
                print(f"Не удалось извлечь цены для {item['name']}")
                
        except Exception as e:
            print(f"Ошибка при запросе товара {item['name']}: {e}")

if __name__ == "__main__":
    check_kaspi_prices()
