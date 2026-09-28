import os
import urllib.request
import json

# Получаем ключи из сейфа GitHub
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram_message(text):
    """Функция отправки сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({"chat_id": CHAT_ID, "text": text}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            print("Сообщение успешно отправлено!")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def main():
    # Пока тестовое сообщение, чтобы убедиться, что всё работает
    send_telegram_message("🤖 Привет! Ваш бот для Kaspi успешно запущен и готов к работе!")

if __name__ == "__main__":
    main()
