import time
import random
import requests # или те библиотеки, которые ты используешь для запросов

# 1. Твой список из 340 товаров (или загрузка твоего списка)
all_products = [...] # здесь твой реальный список товаров

def chunk_list(lst, chunk_size):
    """Делит большой список на пачки по 60 штук"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def main():
    print(f"Старт работы бота. Всего товаров: {len(all_products)}")
    
    # Делим на пачки
    batches = list(chunk_list(all_products, 60))
    total_batches = len(batches)
    
    for batch_index, batch in enumerate(batches, start=1):
        print(f"Обработка пачки {batch_index} из {total_batches}...")
        
        for product in batch:
            # === СЮДА ВСТАВЬ СВОЙ СТАРЫЙ КОД ОТПРАВКИ ОДНОГО ТОВАРА ===
            # Например: response = requests.post(...)
            print(f"Обрабатываем товар: {product}")
            
            # Микропауза между товарами внутри пачки (от 2 до 5 секунд)
            time.sleep(random.uniform(2.0, 5.0))
            
        # Пауза 5 минут (300 секунд) между пачками (кроме последней)
        if batch_index < total_batches:
            print("Пачка завершена. Ждем 5 минут...")
            time.sleep(300)

    print("Все товары успешно обработаны!")

if __name__ == "__main__":
    main()
