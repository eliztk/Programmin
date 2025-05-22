#Завдання 1: Робота з текстом
def count_words(text):
    text = text.lower()

    for symbol in ',.':
        text = text.replace(symbol, '')

    words = text.split()

    word_count = {}

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count

text = "Кіт стрибнув на стіл, кіт вкрав котлету, кіт сховався, кіт відкусив котлету."
result = count_words(text)

print("Список слів і кількість їх появ:")
print(result)

frequent_words = [word for word, count in result.items() if count > 3]

print("\nСлова, які з'являються більше 3 разів:")
print(frequent_words)

print()

#Завдання 2: Інвентаризація продуктів
products = {
    "апельсини": 15,
    "яблука": 3,
    "макарони": 13,
    "йогурти": 4
}

def updates_products(product, amount):

    if product in products:
        products[product] += amount
    else:
        products[product] = amount

    if products[product] < 0:
        products[product] = 0

updates_products("апельсини", 5)
updates_products("макарони", -2)
updates_products("сири", 8)
updates_products("сири", -1)

print("Оновлений склад продуктів:")
for product, quantity in products.items():
    print(f"{product}: {quantity}")

low_number = [product for product, quantity in products.items() if quantity < 5]

print("\nПродукти, кількість яких менше 5 штук:")
print(low_number)

print()

#Завдання 3: Статистика продажів
sales = [
    {"продукт": "апельсини", "кількість": 30, "ціна": 25},
    {"продукт": "яблука", "кількість": 25, "ціна": 15},
    {"продукт": "макарони", "кількість": 40, "ціна": 20},
    {"продукт": "йогурти", "кількість": 50, "ціна": 30},
    {"продукт": "сири", "кількість": 70, "ціна": 50}
]

def calculate_income(sales_list):
    income = {}
    for sale in sales_list:
        product = sale["продукт"]
        quantity = sale["кількість"]
        price = sale["ціна"]
        total = quantity * price

        if product in income:
            income[product] += total
        else:
            income[product] = total
    return income

income_by_product = calculate_income(sales)

print("Дохід для кожного продукту:")
for product, income in income_by_product.items():
    print(f"{product}: {income} грн")

top_products = [product for product, income in income_by_product.items() if income > 1000]

print("\nПродукти, що принесли більше ніж 1000 грн:")
print(top_products)

print()

#Завдання 4: Система управління задачами
tasks = {
    "Виконати лабораторну роботу": "в процесі",
    "Виконати практичну роботу": "очікує",
    "Зробити проект": "виконано",
    "Пройти тести": "очікує",
    "Написати курсову": "виконано"
}

def add_task(name, status):
    tasks[name] = status
    print(f"Задача '{name}' додана зі статусом: {status}")

def delete_task(name, status):
    if name in tasks:
        del tasks[name]
        print(f"Задача '{name}' зі статусом: '{status}' видалена.")
    else:
        print(f"Задача '{name}' зі статусом: '{status}' не знайдена.")

def updates_task_status(name, new_status):
    if name in tasks:
        tasks[name] = new_status
        print(f"Статус задачі '{name}' оновлено на: {new_status}")
    else:
        print(f"Задача '{name}' не знайдена.")

add_task("Написати конспекти", "очікує")
delete_task("Написати курсову", "виконано")
updates_task_status("Виконати практичну роботу", "в процесі")

print("\nСписок усіх задач:")
for name, status in tasks.items():
    print(f"{name}: {status}")

waiting_tasks = [name for name, status in tasks.items() if status == "очікує"]

print("\nЗадачі зі статусом 'очікує':")
print(waiting_tasks)
print()

#Завдання 5: Аутентифікація користувачів
import hashlib

users = {
    "Ol4Bond": {
        "password": hashlib.md5("H02Owr".encode()).hexdigest(),
        "name": "Олександра Бондаренко"
    },
    "Andrey547": {
        "password": hashlib.md5("Tom5Sr".encode()).hexdigest(),
        "name": "Андрій Лоза"
    },
    "Tanyka05": {
        "password": hashlib.md5("pass40my".encode()).hexdigest(),
        "name": "Тетяна Карась"
    }
}

def authentication():
    login = input("Введіть логін: ")
    password = input("Введіть пароль: ")

    if login in users:

        password_hash = hashlib.md5(password.encode()).hexdigest()

        if password_hash == users[login]["password"]:
            print(f"Вітаю, {users[login]['name']}! Ви успішно увійшли!")
        else:
            print("Невірний пароль!")
    else:
        print("Користувача з таким логіном не знайдено!")

authentication()


