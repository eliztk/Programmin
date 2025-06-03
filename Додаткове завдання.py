import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'MyDatabase.db'

def create_Table():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS EventSources (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            location TEXT,
            type TEXT
        );
    ''')
    connection.commit()
    connection.close()

def insert_EventSources():
    event_sources = [
        ("VPN_Gateway", "109.0.50.1", "VPN"),
        ("Cloud_Security_Alerts", "cloud.service.com", "Cloud Security"),
        ("Email_Filter_Reports", "196.0.1.21", "Email Filter"),
        ("Malware_Analysis_Logs", "172.13.10.18", "Malware Analysis"),
        ("DNS_Traffic_Monitor", "dns.monitor.local", "DNS Monitor")
    ]
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM EventSources')

    for name, location, type_ in event_sources:
        cursor.execute(f'''
            INSERT INTO EventSources (name, location, type)
            VALUES (?, ?, ?)
        ''', (name, location, type_))

    connection.commit()
    connection.close()

def create_EventTypes_table():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS EventTypes (
            id INTEGER PRIMARY KEY,
            type_name TEXT UNIQUE,
            severity TEXT
        );
    ''')

    connection.commit()
    connection.close()

def insert_EventTypes():
    event_types = [
        ("Login Success", "Informational"),
        ("Login Failed", "Warning"),
        ("Insert Incorrect Data", "Critical"),
        ("Unusual Behaviour", "Warning")
    ]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM EventTypes")

    for type_name, severity in event_types:
        cursor.execute('''
            INSERT INTO EventTypes (type_name, severity)
            VALUES (?, ?)
        ''', (type_name, severity))

    connection.commit()
    connection.close()


def create_SecurityEvents_Table():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SecurityEvents (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME,
            source_id INTEGER,
            event_type_id INTEGER,
            message TEXT,
            ip_address TEXT,
            username TEXT,
            FOREIGN KEY (source_id) REFERENCES EventSources(id),
            FOREIGN KEY (event_type_id) REFERENCES EventTypes(id)
        );
    ''')
    connection.commit()
    connection.close()

def insert_SecurityEvents():
    events = [
        ("2025-06-03 11:25:03", 1, 1, "Користувач admin успішно увійшов в систему", "194.168.1.3", "admin"),
        ("2025-06-03 11:48:34", 1, 1, "Користувач KarinBondar47 успішно увійшов в систему", "172.0.5.17", "KarinBondar47"),
        ("2025-06-03 11:50:29", 3, 3, "Користувач ввів некоректні дані для входу через email", None, "user08"),
        ("2025-06-03 14:01:54", 1, 4, "Виявлено незвичайну поведінку VPN клієнта", "198.0.8.21", None),
        ("2025-06-03 16:58:56", 2, 2, "Користувач guest з хмарного інтерфейсу не зміг увійти в систему", "154.45.1.33", "guest"),
        ("2025-06-05 07:45:36", 4, 3, "Виявлено шкідливий виконуваний файл в системі", "10.10.6.27", "MalwUser"),
        ("2025-06-05 10:39:19", 5, 1, "Звичайний DNS-запит до google.com", "192.168.100.4", "system_service"),
        ("2025-06-05 18:31:59", 3, 3, "Виявлено шкідливе корисне навантаження у вкладенні email", None, "user284"),
        ("2025-06-12 19:38:29", 2, 1, "Користувач MaxSukhar20 не зміг увійти в систему", "128.0.4.23", "MaxSukhar20"),
        ("2025-06-12 20:01:37", 4, 2, "Виявлено помилку під час аналізу архіву з підозрілим вмістом", None, "userMalw27"),

    ]

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    for timestamp, source_id, event_type_id, message, ip_address, username in events:
        cursor.execute(f'''
            INSERT INTO SecurityEvents (
                timestamp, source_id, event_type_id, message, ip_address, username
            )
            VALUES (
                '{timestamp}', {source_id}, {event_type_id}, '{message}',
                {f"'{ip_address}'" if ip_address else 'NULL'},
                {f"'{username}'" if username else 'NULL'}
            )
        ''')

    connection.commit()
    connection.close()

def registration_EventSource():
    name = input("Введіть назву джерела подій: ").strip()
    location = input("Введіть розташування джерела: ").strip()
    type_ = input("Введіть тип джерела: ").strip()

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO EventSources (name, location, type)
                VALUES (?, ?, ?)
            ''', (name, location, type_))
            conn.commit()
            print("Джерело подій було успішно додано")
    except sqlite3.IntegrityError:
        print("Помилка: Дане джерело вже існує або дані є некоректними")


def registration_EventType():
    type_name = input("Введіть назву типу події: ").strip()
    severity = input("Введіть серйозність типу події: ").strip()

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO EventTypes (type_name, severity)
                VALUES (?, ?)
            ''', (type_name, severity))
            conn.commit()
            print("Тип події було успішно додано")
    except sqlite3.IntegrityError:
        print("Помилка: Даний тип вже існує або дані є некоректними")

def record_SecurityEvent():
    try:
        source_id = int(input("Введіть id джерела події: "))
        event_type_id = int(input("Введіть id типу події: "))
        message = input("Введіть опис події: ").strip()
        ip_address = input("IP-адреса (за відсутності натискайте Enter): ").strip()
        username = input("Ім’я користувача (за відсутності натискайте Enter): ").strip()

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO SecurityEvents (
                    timestamp, source_id, event_type_id, message, ip_address, username
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                timestamp,
                source_id,
                event_type_id,
                message,
                ip_address if ip_address else None,
                username if username else None
            ))
            conn.commit()
            print(f"Подія була записана ({timestamp}).")
    except ValueError:
        print("Помилка: id повинно бути числом")
    except sqlite3.IntegrityError:
        print("Помилка: Джерела або типу події не існує")

def get_LoginFailed_last24h():
    print("\nПодії 'Login Failed' за останні 24 години:")
    now = datetime.now()
    day_ago = now - timedelta(hours=24)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, ip_address, username, message
            FROM SecurityEvents
            JOIN EventTypes ON SecurityEvents.event_type_id = EventTypes.id
            WHERE EventTypes.type_name = 'Login Failed'
              AND datetime(timestamp) >= datetime(?)
            ORDER BY timestamp DESC
        ''', (day_ago.strftime('%Y-%m-%d %H:%M:%S'),))
        rows = cursor.fetchall()
        for row in rows:
            print(row)

def detect_PotentialAttack():
    print("\nПотенційні атаки підбору пароля (більше 5 спроб за годину):")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ip_address,
                   strftime('%Y-%m-%d %H:00:00', timestamp) AS hour_block,
                   COUNT(*) AS attempts
            FROM SecurityEvents
            JOIN EventTypes ON SecurityEvents.event_type_id = EventTypes.id
            WHERE EventTypes.type_name = 'Login Failed'
              AND ip_address IS NOT NULL
            GROUP BY ip_address, hour_block
            HAVING attempts >= 5
            ORDER BY attempts DESC
        ''')
        rows = cursor.fetchall()
        for row in rows:
            print(f"IP: {row[0]}, Година: {row[1]}, Спроб: {row[2]}")

def get_CriticalEvents_by_source():
    print("\nПодії з серйозністю 'Critical' за останній тиждень, згруповані за джерелом:")
    week_ago = datetime.now() - timedelta(days=7)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT EventSources.name, COUNT(*) AS event_count
            FROM SecurityEvents
            JOIN EventTypes ON SecurityEvents.event_type_id = EventTypes.id
            JOIN EventSources ON SecurityEvents.source_id = EventSources.id
            WHERE EventTypes.severity = 'Critical'
              AND datetime(timestamp) >= datetime(?)
            GROUP BY EventSources.name
            ORDER BY event_count DESC
        ''', (week_ago.strftime('%Y-%m-%d %H:%M:%S'),))
        rows = cursor.fetchall()
        for row in rows:
            print(f"Джерело: {row[0]}, Подій: {row[1]}")

def search_keyword_in_messages():
    keyword = input("Введіть ключове слово для пошуку в повідомленнях: ").strip()
    if not keyword:
        print("Ключове слово не може бути порожнім")
        return
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, message, ip_address, username
            FROM SecurityEvents
            WHERE message LIKE ?
            ORDER BY timestamp DESC
        ''', (f'%{keyword}%',))
        rows = cursor.fetchall()
        if not rows:
            print("Нічого не було знайдено.")
        else:
            print(f"\nРезультати пошуку за ключовим словом: '{keyword}'")
            for row in rows:
                print(row)

create_Table()
insert_EventSources()

create_EventTypes_table()
insert_EventTypes()

create_SecurityEvents_Table()
insert_SecurityEvents()

registration_EventSource()
registration_EventType()
record_SecurityEvent()

get_LoginFailed_last24h()
detect_PotentialAttack()
get_CriticalEvents_by_source()
search_keyword_in_messages()
