import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_table():
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

def add_user(login, password, full_name):
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()

    hashed_password = hash_password(password)

    cursor.execute(f'''
    INSERT INTO Users (login, password, full_name)
    VALUES ('{login}', '{hashed_password}', '{full_name}')
    ''')

    connection.commit()
    connection.close()
    print(f"Користувач {login} був доданий.")

def update_password(login, new_password):
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()

    hashed_password = hash_password(new_password)

    cursor.execute(f'''
    UPDATE Users SET password = '{hashed_password}'
    WHERE login = '{login}'
    ''')

    if cursor.rowcount == 0:
        print(" Користувач не був знайдений.")
    else:
        print(f" Пароль для {login} був оновлений.")

    connection.commit()
    connection.close()

def authenticate_user(login, password):
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()

    hashed_password = hash_password(password)

    cursor.execute(f'''
    SELECT * FROM Users
    WHERE login = '{login}' AND password = '{hashed_password}'
    ''')

    result = cursor.fetchone()

    if result:
        print(f" {result[3]}, ви успішно увійшли!")
    else:
        print(" Невірний логін або пароль.")

    connection.close()

def main():
    create_table()

    print("\n1. Додавання нового користувача")
    print("2. Оновлення паролю користувача")
    print("3. Перевірка автентифікації")

    choice = input("Ваш вибір: ")

    if choice == '1':
        login = input("Логін: ")
        password = input("Пароль: ")
        full_name = input("Повне ім'я: ")
        add_user(login, password, full_name)

    elif choice == '2':
        login = input("Логін: ")
        new_password = input("Новий пароль: ")
        update_password(login, new_password)

    elif choice == '3':
        login = input("Логін: ")
        password = input("Пароль: ")
        authenticate_user(login, password)

    else:
        print(" Невірний вибір. Запустіть програму ще раз.")

if __name__ == '__main__':
    main()


