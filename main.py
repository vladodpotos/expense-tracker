import json
import os
from datetime import datetime, timedelta

DATA_FILE = "expenses.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=2)

def add_purchase():
    expenses = load_data()
    
    print("\n--- Добавление покупки ---")
    name = input("Название товара: ").strip()
    
    while True:
        try:
            price = float(input("Цена (в рублях): "))
            if price > 0:
                break
            print("Цена должна быть больше 0")
        except ValueError:
            print("Введите число")
    
    category = input("Категория (Продукты, Транспорт, Одежда и т.д.): ").strip()
    if not category:
        category = "Прочее"
    
    date = input("Дата покупки (ГГГГ-ММ-ДД): ").strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    expenses.append({
        "name": name,
        "price": price,
        "category": category,
        "date": date
    })
    
    save_data(expenses)
    print(f"Покупка '{name}' добавлена!")

def view_purchases():
    expenses = load_data()
    
    if not expenses:
        print("\nСписок покупок пуст")
        return
    
    print("\n" + "="*50)
    print("СПИСОК ПОКУПОК")
    print("="*50)
    
    total = 0
    for i, item in enumerate(expenses, 1):
        print(f"{i}. {item['name']} - {item['price']} ₽")
        print(f"   Категория: {item['category']}, Дата: {item['date']}\n")
        total += item['price']
    
    print(f"Итого: {total} ₽")

def total_spent():
    expenses = load_data()
    
    if not expenses:
        print("\nНет данных о покупках")
        return
    
    total = sum(item['price'] for item in expenses)
    print(f"\nОбщая сумма расходов: {total} ₽")

def spent_by_category():
    expenses = load_data()
    
    if not expenses:
        print("\nНет данных о покупках")
        return
    
    categories = {}
    for item in expenses:
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + item['price']
    
    print("\n--- Расходы по категориям ---")
    for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"{cat}: {amount} ₽")

def spent_by_period():
    expenses = load_data()
    
    if not expenses:
        print("\nНет данных о покупках")
        return
    
    print("\n--- Расходы за период ---")
    print("1. День")
    print("2. Неделя")
    print("3. Месяц")
    
    choice = input("Выберите период: ").strip()
    
    today = datetime.now().date()
    
    if choice == "1":
        start_date = today
        period_name = "сегодня"
    elif choice == "2":
        start_date = today - timedelta(days=7)
        period_name = "за последние 7 дней"
    elif choice == "3":
        start_date = today - timedelta(days=30)
        period_name = "за последние 30 дней"
    else:
        print("Неверный выбор")
        return
    
    total = 0
    count = 0
    for item in expenses:
        item_date = datetime.strptime(item['date'], "%Y-%m-%d").date()
        if item_date >= start_date:
            total += item['price']
            count += 1
    
    print(f"\nРасходы {period_name}: {total} ₽")
    print(f"Количество покупок: {count}")

def main():
    load_data()
    
    while True:
        print("\n" + "="*40)
        print("АНАЛИЗАТОР РАСХОДОВ")
        print("="*40)
        print("1. Добавить покупку")
        print("2. Показать все покупки")
        print("3. Общая сумма расходов")
        print("4. Расходы по категориям")
        print("5. Расходы за период")
        print("6. Выход")
        
        choice = input("\nВыберите пункт: ").strip()
        
        if choice == "1":
            add_purchase()
        elif choice == "2":
            view_purchases()
        elif choice == "3":
            total_spent()
        elif choice == "4":
            spent_by_category()
        elif choice == "5":
            spent_by_period()
        elif choice == "6":
            save_data(load_data())
            print("До свидания!")
            break
        else:
            print("❌ Неверный пункт, попробуйте снова")

if __name__ == "__main__":
    main()