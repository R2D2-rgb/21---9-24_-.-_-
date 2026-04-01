import sqlite3

def create_database():
    # Подключение к базе данных (или создание, если не существует)
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()

    # Включаем поддержку внешних ключей
    cursor.execute("PRAGMA foreign_keys = ON")

    # Удаляем таблицы, если они существуют (в обратном порядке)
    cursor.execute("DROP TABLE IF EXISTS Transactions")
    cursor.execute("DROP TABLE IF EXISTS Accounts")
    cursor.execute("DROP TABLE IF EXISTS Loans")
    cursor.execute("DROP TABLE IF EXISTS Clients")

    # Создаем таблицу Клиенты
    cursor.execute('''
        CREATE TABLE Clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT UNIQUE,
            email TEXT UNIQUE,
            address TEXT,
            passport_data TEXT UNIQUE,
            registration_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Создаем таблицу Счета
    cursor.execute('''
        CREATE TABLE Accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            account_number TEXT UNIQUE NOT NULL,
            account_type TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0,
            opening_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE
        )
    ''')

    # Создаем таблицу Кредиты
    cursor.execute('''
        CREATE TABLE Loans (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            account_id INTEGER,
            loan_amount REAL NOT NULL,
            interest_rate REAL NOT NULL,
            term_months INTEGER NOT NULL,
            issue_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE,
            FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE SET NULL
        )
    ''')

    # Создаем таблицу Транзакции
    cursor.execute('''
        CREATE TABLE Transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
        )
    ''')

    # Заполняем таблицу Клиенты
    clients_data = [
        ('Иванов Иван Иванович', '+79123456789', 'ivanov@example.com', 'ул. Ленина, 10', '1234 567890'),
        ('Петров Петр Петрович', '+79234567890', 'petrov@example.com', 'ул. Пушкина, 20', '2345 678901'),
        ('Сидоров Сидор Сидорович', '+79345678901', 'sidorov@example.com', 'ул. Гоголя, 30', '3456 789012'),
        ('Кузнецова Анна Васильевна', '+79456789012', 'kuznetsova@example.com', 'ул. Толстого, 40', '4567 890123'),
        ('Васильев Василий Васильевич', '+79567890123', 'vasiliev@example.com', 'ул. Чехова, 50', '5678 901234')
    ]
    cursor.executemany("INSERT INTO Clients (full_name, phone, email, address, passport_data) VALUES (?, ?, ?, ?, ?)", clients_data)

    # Заполняем таблицу Счета
    accounts_data = [
        (1, '40817810100000000001', 'debit', 10000.00),
        (1, '40817810100000000002', 'credit', 50000.00),
        (2, '40817810100000000003', 'debit', 15000.00),
        (3, '40817810100000000004', 'debit', 20000.00),
        (4, '40817810100000000005', 'deposit', 100000.00),
        (5, '40817810100000000006', 'debit', 8000.00)
    ]
    cursor.executemany("INSERT INTO Accounts (client_id, account_number, account_type, balance) VALUES (?, ?, ?, ?)", accounts_data)

    # Заполняем таблицу Кредиты
    loans_data = [
        (1, 2, 100000.00, 12.5, 24),
        (2, 3, 50000.00, 15.0, 12),
        (3, 4, 75000.00, 13.0, 18),
        (4, 5, 200000.00, 11.0, 36),
        (5, 6, 30000.00, 14.5, 12)
    ]
    cursor.executemany("INSERT INTO Loans (client_id, account_id, loan_amount, interest_rate, term_months) VALUES (?, ?, ?, ?, ?)", loans_data)

    # Заполняем таблицу Транзакции
    transactions_data = [
        (1, 'deposit', 5000.00, 'Зарплата'),
        (1, 'withdrawal', 2000.00, 'Покупка'),
        (2, 'deposit', 10000.00, 'Перевод'),
        (3, 'withdrawal', 3000.00, 'Оплата услуг'),
        (4, 'deposit', 15000.00, 'Возврат'),
        (5, 'withdrawal', 1000.00, 'Коммунальные платежи'),
        (6, 'deposit', 2000.00, 'Проценты'),
        (1, 'transfer', 5000.00, 'Перевод на счет 2'),
        (2, 'transfer', 5000.00, 'Перевод со счета 1'),
        (3, 'withdrawal', 1000.00, 'Снятие наличных')
    ]
    cursor.executemany("INSERT INTO Transactions (account_id, transaction_type, amount, description) VALUES (?, ?, ?, ?)", transactions_data)

    # Сохраняем изменения
    conn.commit()

    # Финальный запрос с JOIN
    cursor.execute('''
        SELECT
            c.full_name AS "Клиент",
            a.account_number AS "Номер счета",
            a.account_type AS "Тип счета",
            a.balance AS "Баланс",
            l.loan_amount AS "Сумма кредита",
            t.transaction_date AS "Дата транзакции",
            t.transaction_type AS "Тип транзакции",
            t.amount AS "Сумма транзакции"
        FROM Clients c
        JOIN Accounts a ON c.client_id = a.client_id
        LEFT JOIN Loans l ON c.client_id = l.client_id
        LEFT JOIN Transactions t ON a.account_id = t.account_id
        ORDER BY c.full_name, t.transaction_date DESC
    ''')

    # Выводим результаты
    print("\nОтчет по банковским операциям:")
    print("-" * 100)
    for row in cursor.fetchall():
        print(row)

    # Закрываем соединение
    conn.close()

if __name__ == "__main__":
    create_database()
