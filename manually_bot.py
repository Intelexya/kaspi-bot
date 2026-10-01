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
    },
    {
        "name": "HYUNDAI / KIA буфер 8219128010 Hyundai Accent",
        "url": "https://kaspi.kz/shop/p/hyundai-kia-bufer-8219128010-hyundai-accent-146549204/?c=750000000",
        "my_price": 470
    },
    {
        "name": "K2 крышка топливного бака 7730006040",
        "url": "https://kaspi.kz/shop/p/k2-kryshka-toplivnogo-baka-7730006040-153968849/?c=750000000",
        "my_price": 4010
    },
    {
        "name": "Крепление 71111179444 BMW 3-Series 320, 3-Series 325, 3-Series 328, 3-Series 330, 5-Series 520, 5-Series 525, 5-Series 528, 5-Series 530, 7-Series 728",
        "url": "https://kaspi.kz/shop/p/kreplenie-71111179444-bmw-3-series-320-3-series-325-3-series-328-3-series-330-5-series-520-5-series-525-5-series-528-5-series-530-7-series-728-7-series-730-7-series-732-7-series-735-7-series-740-7-series-745-119716896/?c=750000000",
        "my_price": 1918
    },
    {
        "name": "K2 ниппель для кондиционера 96800053",
        "url": "https://kaspi.kz/shop/p/k2-nippel-dlja-konditsionera-96800053-162491581/?c=750000000",
        "my_price": 1200
    },
    {
        "name": "Ограничитель 82191-28010 Hyundai Accent",
        "url": "https://kaspi.kz/shop/p/ogranichitel-82191-28010-hyundai-accent-133383830/?c=750000000",
        "my_price": 470
    },
    {
        "name": "Концевик 84231-60070 Toyota Land Cruiser Prado",
        "url": "https://kaspi.kz/shop/p/kontsevik-84231-60070-toyota-land-cruiser-prado-131085948/?c=750000000",
        "my_price": 2510
    },
    {
        "name": "Oshide ограничитель C-3247 Nissan FX35",
        "url": "https://kaspi.kz/shop/p/oshide-ogranichitel-c-3247-nissan-fx35-124370815/?c=750000000",
        "my_price": 400
    },
    {
        "name": "PATRON форсунка омывателя P210001 Seat Rapid",
        "url": "https://kaspi.kz/shop/p/patron-forsunka-omyvatelja-p210001-seat-rapid-114888897/?c=750000000",
        "my_price": 1190
    },
    {
        "name": "K2 фиксатор MR532555",
        "url": "https://kaspi.kz/shop/p/k2-fiksator-mr532555-144087758/?c=750000000",
        "my_price": 3099
    },
    {
        "name": "K2 кнопка 81260C1010 Hyundai Sonata",
        "url": "https://kaspi.kz/shop/p/k2-knopka-81260c1010-hyundai-sonata-142184049/?c=750000000",
        "my_price": 4600
    },
    {
        "name": "Vernet крышка расширительного бачка RC0184",
        "url": "https://kaspi.kz/shop/p/vernet-kryshka-rasshiritel-nogo-bachka-rc0184-124257495/?c=750000000",
        "my_price": 1338
    },
    {
        "name": "HYUNDAI / KIA ручка открывания капота 8118034000RY",
        "url": "https://kaspi.kz/shop/p/hyundai-kia-ruchka-otkryvanija-kapota-8118034000ry-145608724/?c=750000000",
        "my_price": 3628
    },
    {
        "name": "Блок кнопок 84820-33230",
        "url": "https://kaspi.kz/shop/p/blok-knopok-84820-33230-139487957/?c=750000000",
        "my_price": 12998
    },
    {
        "name": "Заглушка 90950 01960 Daihatsu CT 200h",
        "url": "https://kaspi.kz/shop/p/zaglushka-90950-01960-daihatsu-ct-200h-165931358/?c=750000000",
        "my_price": 1500
    },
    {
        "name": "JP GROUP крышка омывателя 1198600300 Audi A1",
        "url": "https://kaspi.kz/shop/p/jp-group-kryshka-omyvatelja-1198600300-audi-a1-129686813/?c=750000000",
        "my_price": 1790
    },
    {
        "name": "JPS крышка маслозаливной горловины 12180-28010",
        "url": "https://kaspi.kz/shop/p/jps-kryshka-maslozalivnoi-gorloviny-12180-28010-114151447/?c=750000000",
        "my_price": 1500
    },
    {
        "name": "K2 фиксатор 5890860060",
        "url": "https://kaspi.kz/shop/p/k2-fiksator-5890860060-144087307/?c=750000000",
        "my_price": 3300
    },
    {
        "name": "K2 крючок солнцезащитного козырька 3B0857561B",
        "url": "https://kaspi.kz/shop/p/k2-krjuchok-solntsezaschitnogo-kozyr-ka-3b0857561b-166930409/?c=750000000",
        "my_price": 2000
    },
    {
        "name": "Заглушка 85292-0F010 Lexus Corolla",
        "url": "https://kaspi.kz/shop/p/zaglushka-85292-0f010-lexus-corolla-133966868/?c=750000000",
        "my_price": 1180
    },
    {
        "name": "Ручка КПП для Volkswagen Passat 1989-1997 черный",
        "url": "https://kaspi.kz/shop/p/ruchka-kpp-dlja-volkswagen-passat-1989-1997-chernyi-138763286/?c=750000000",
        "my_price": 3997
    },
    {
        "name": "Крышка клапана кондиционера А/С -HL 2 шт",
        "url": "https://kaspi.kz/shop/p/kryshka-klapana-konditsionera-a-s--hl-2-sht-120023581/?c=750000000",
        "my_price": 498
    },
    {
        "name": "ABS отбойник 817381J000 Hyundai Accent",
        "url": "https://kaspi.kz/shop/p/abs-otboinik-817381j000-hyundai-accent-164387759/?c=750000000",
        "my_price": 750
    },
    {
        "name": "TORSO 10150866 упор капота для универсальный черный",
        "url": "https://kaspi.kz/shop/p/torso-10150866-upor-kapota-dlja-universal-nyi-chernyi-130245275/?c=750000000",
        "my_price": 1739
    },
    {
        "name": "Ручка ME81180340009RY Hyundai Accent",
        "url": "https://kaspi.kz/shop/p/ruchka-me81180340009ry-hyundai-accent-124302867/?c=750000000",
        "my_price": 3799
    },
    {
        "name": "SAT крышка маслозаливной горловины ST-308-0001",
        "url": "https://kaspi.kz/shop/p/sat-kryshka-maslozalivnoi-gorloviny-st-308-0001-122351055/?c=7500000030",
        "my_price": 1859
    },
    {
        "name": "OEM крючок солнцезащитного козырька 74348-06030",
        "url": "https://kaspi.kz/shop/p/oem-krjuchok-solntsezaschitnogo-kozyr-ka-74348-06030-110700910/?c=750000000",
        "my_price": 1460
    },
    {
        "name": "ABS втулка 9048016049",
        "url": "https://kaspi.kz/shop/p/abs-vtulka-9048016049-164636838/?c=750000000",
        "my_price": 1299
    },
    {
        "name": "Заглушка 90950-01958 Lexus ES 200",
        "url": "https://kaspi.kz/shop/p/zaglushka-90950-01958-lexus-es-200-171960642/?c=750000000",
        "my_price": 1350
    },
    {
        "name": "SRR крышка топливного бака 77300-33070",
        "url": "https://kaspi.kz/shop/p/srr-kryshka-toplivnogo-baka-77300-33070-116309998/?c=750000000",
        "my_price": 3497
    },
    {
        "name": "Крышка омывателя 86615AA060",
        "url": "https://kaspi.kz/shop/p/kryshka-omyvatelja-86615aa060-135444551/?c=750000000",
        "my_price": 1345
    },
    {
        "name": "Ручка 83660-4H100 Hyundai H1",
        "url": "https://kaspi.kz/shop/p/ruchka-83660-4h100-hyundai-h1-139693271/?c=750000000",
        "my_price": 2700
    },
    {
        "name": "Крышка топливного бака 7730006040",
        "url": "https://kaspi.kz/shop/p/kryshka-toplivnogo-baka-7730006040-154439341/?c=750000000",
        "my_price": 5700
    },
    {
        "name": "K2 крышка омывателя 8531626030",
        "url": "https://kaspi.kz/shop/p/k2-kryshka-omyvatelja-8531626030-142247823/?c=750000000",
        "my_price": 1791
    },
    {
        "name": "WXQP крючок солнцезащитного козырька 74348-33040",
        "url": "https://kaspi.kz/shop/p/wxqp-krjuchok-solntsezaschitnogo-kozyr-ka-74348-33040-165374614/?c=750000000",
        "my_price": 1490
    },
    {
        "name": "HYUNDAI / KIA ручка открывания капота 8118034000WK",
        "url": "https://kaspi.kz/shop/p/hyundai-kia-ruchka-otkryvanija-kapota-8118034000wk-144207627/?c=750000000",
        "my_price": 3700
    },
    {
        "name": "Чехол на рычаг КПП в виде толстовки, для МКПП и АКПП, зимний, антискользящий, цвета синий",
        "url": "https://kaspi.kz/shop/p/chehol-na-rychag-kpp-v-vide-tolstovki-dlja-mkpp-i-akpp-zimnii-antiskol-zjaschii-tsveta-sinii-i-krasnyi-otpravljajutsja-sluchaino-155610618/?c=750000000",
        "my_price": 1498
    },
    {
        "name": "AE крышка расширительного бачка 16405-31070",
        "url": "https://kaspi.kz/shop/p/ae-kryshka-rasshiritel-nogo-bachka-16405-31070-153776975/?c=750000000",
        "my_price": 3300
    },
    {
        "name": "K2 крючок солнцезащитного козырька 88217S01A01ZA",
        "url": "https://kaspi.kz/shop/p/k2-krjuchok-solntsezaschitnogo-kozyr-ka-88217s01a01za-153968848/?c=750000000",
        "my_price": 2000
    },
    {
        "name": "A.B.S. кнопка 81260-1W220 Hyundai Accent",
        "url": "https://kaspi.kz/shop/p/a-b-s-knopka-81260-1w220-hyundai-accent-153829245/?c=750000000",
        "my_price": 4990
    },
    {
        "name": "Блок кнопок 84820-06100",
        "url": "https://kaspi.kz/shop/p/blok-knopok-84820-06100-114197160/?c=750000000",
        "my_price": 10900
    },
    {
        "name": "TAIWAN крышка омывателя 763333",
        "url": "https://kaspi.kz/shop/p/taiwan-kryshka-omyvatelja-763333-119710822/?c=750000000",
        "my_price": 1020
    },
    {
        "name": "SAILING ручка MBL23003232",
        "url": "https://kaspi.kz/shop/p/sailing-ruchka-mbl23003232-109331640/?c=750000000",
        "my_price": 3400
    },
    {
        "name": "OSSCA крышка маслозаливной горловины 26510-26600",
        "url": "https://kaspi.kz/shop/p/ossca-kryshka-maslozalivnoi-gorloviny-26510-26600-124218993/?c=750000000",
        "my_price": 1890
    },
    {
        "name": "K2 крышка омывателя 85316-06021",
        "url": "https://kaspi.kz/shop/p/k2-kryshka-omyvatelja-85316-06021-142247760/?c=750000000",
        "my_price": 1874
    },
    {
        "name": "Блок кнопок 935701R410",
        "url": "https://kaspi.kz/shop/p/blok-knopok-935701r410-132802452/?c=750000000",
        "my_price": 11000
    },
    {
        "name": "Zebra крючок солнцезащитного козырька 7434833040B",
        "url": "https://kaspi.kz/shop/p/zebra-krjuchok-solntsezaschitnogo-kozyr-ka-7434833040b-164080156/?c=750000000",
        "my_price": 2000
    },
    {
        "name": " ",
        "url": " ",
        "my_price": 
    },
    {
        "name": " ",
        "url": " ",
        "my_price": 
    },
    {
        "name": " ",
        "url": " ",
        "my_price": 
    },
    {
        "name": " ",
        "url": " ",
        "my_price": 
    },
    {
        "name": " ",
        "url": " ",
        "my_price": 
    },
    {
        "name": " ",
        "url": " ",
        "my_price": 
    },
    {
        "name": " ",
        "url": " ",
        "my_price": 
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
                    status = f"❌ *Вы не первый!*\n   Низкая цена: {best_price} ₸ | Ваша: {item['my_price']} ₸"
                else:
                    status = f"✅ *Вы первый!*\n   Низкая цена: {best_price} ₸ | Ваша: {item['my_price']} ₸"
            else:
                status = "⚠️ Не удалось определить цену"
            
            report_lines.append(f"{index}️⃣ *{item['name']}*\n{status}\n")
        except Exception as e:
            report_lines.append(f"{index}️⃣ *{item['name']}*\n⚠️ Ошибка проверки\n")

    full_report = "\n".join(report_lines)
    send_telegram_message(full_report)

if __name__ == "__main__":
    generate_report()
