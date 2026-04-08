import sqlite3
from db import get_connection


def add_client(full_name, phone, email, address, passport_data):
    """Добавляет нового клиента"""
    query = """
        INSERT INTO Clients (full_name, phone, email, address, passport_data) 
        VALUES (?, ?, ?, ?, ?)
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (full_name, phone, email, address, passport_data))
            conn.commit()
            print(f"✅ Клиент '{full_name}' успешно добавлен! ID: {cursor.lastrowid}")
            return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        if "phone" in str(e):
            print("❌ Ошибка: Клиент с таким номером телефона уже существует!")
        elif "email" in str(e):
            print("❌ Ошибка: Клиент с таким email уже существует!")
        elif "passport_data" in str(e):
            print("❌ Ошибка: Клиент с таким паспортом уже существует!")
        else:
            print(f"❌ Ошибка целостности: {e}")
    except sqlite3.Error as e:
        print(f"❌ Ошибка БД: {e}")


def open_account(client_id, account_type, initial_balance=0):
    """Открывает новый счёт для клиента"""
    import random
    account_number = f"40817810{random.randint(1000000000, 9999999999)}"

    query = """
        INSERT INTO Accounts (client_id, account_number, account_type, balance, status) 
        VALUES (?, ?, ?, ?, 'active')
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (client_id, account_number, account_type, initial_balance))
            conn.commit()
            print(f"✅ Счёт {account_number} ({account_type}) открыт! Баланс: {initial_balance} RUB")
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"❌ Ошибка открытия счёта: {e}")


def perform_transaction(account_id, transaction_type, amount, description=""):
    """Выполняет транзакцию по счёту"""
    if amount <= 0:
        print("❌ Сумма транзакции должна быть положительной!")
        return False

    # Проверяем тип транзакции
    valid_types = ['deposit', 'withdrawal', 'transfer']
    if transaction_type not in valid_types:
        print(f"❌ Неверный тип транзакции! Доступны: {', '.join(valid_types)}")
        return False

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Для снятия средств проверяем баланс
            if transaction_type in ['withdrawal', 'transfer']:
                cursor.execute("SELECT balance FROM Accounts WHERE account_id = ?", (account_id,))
                row = cursor.fetchone()
                if not row:
                    print("❌ Счёт не найден!")
                    return False
                if row['balance'] < amount:
                    print(f"❌ Недостаточно средств! Доступно: {row['balance']} RUB")
                    return False
                # Списываем средства
                cursor.execute("UPDATE Accounts SET balance = balance - ? WHERE account_id = ?",
                               (amount, account_id))
            elif transaction_type == 'deposit':
                # Пополняем счёт
                cursor.execute("UPDATE Accounts SET balance = balance + ? WHERE account_id = ?",
                               (amount, account_id))

            # Записываем транзакцию
            cursor.execute("""
                INSERT INTO Transactions (account_id, transaction_type, amount, description) 
                VALUES (?, ?, ?, ?)
            """, (account_id, transaction_type, amount, description or f"{transaction_type} на сумму {amount}"))

            conn.commit()

            # Получаем новый баланс
            cursor.execute("SELECT balance FROM Accounts WHERE account_id = ?", (account_id,))
            new_balance = cursor.fetchone()['balance']

            print(f"✅ Транзакция выполнена! Новый баланс: {new_balance} RUB")
            return True
    except sqlite3.Error as e:
        print(f"❌ Ошибка транзакции: {e}")
        return False


def take_loan(client_id, account_id, loan_amount, interest_rate, term_months):
    """Оформляет кредит клиенту"""
    if loan_amount <= 0:
        print("❌ Сумма кредита должна быть положительной!")
        return False

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Проверяем существование клиента и счёта
            cursor.execute("SELECT 1 FROM Clients WHERE client_id = ?", (client_id,))
            if not cursor.fetchone():
                print("❌ Клиент не найден!")
                return False

            cursor.execute("SELECT 1 FROM Accounts WHERE account_id = ? AND client_id = ?",
                           (account_id, client_id))
            if not cursor.fetchone():
                print("❌ Счёт не найден или не принадлежит клиенту!")
                return False

            # Оформляем кредит
            cursor.execute("""
                INSERT INTO Loans (client_id, account_id, loan_amount, interest_rate, term_months, status) 
                VALUES (?, ?, ?, ?, ?, 'active')
            """, (client_id, account_id, loan_amount, interest_rate, term_months))

            # Зачисляем сумму кредита на счёт
            cursor.execute("UPDATE Accounts SET balance = balance + ? WHERE account_id = ?",
                           (loan_amount, account_id))

            # Записываем транзакцию зачисления кредита
            cursor.execute("""
                INSERT INTO Transactions (account_id, transaction_type, amount, description) 
                VALUES (?, 'deposit', ?, 'Зачисление кредита')
            """, (account_id, loan_amount))

            conn.commit()

            monthly_payment = (loan_amount * (interest_rate / 100) / 12) + (loan_amount / term_months)
            print(f"✅ Кредит на {loan_amount} RUB оформлен!")
            print(f"📊 Ставка: {interest_rate}%, срок: {term_months} месяцев")
            print(f"💳 Примерный ежемесячный платёж: {monthly_payment:.2f} RUB")
            return True
    except sqlite3.Error as e:
        print(f"❌ Ошибка оформления кредита: {e}")
        return False


def close_account(account_id):
    """Закрывает счёт (меняет статус)"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Проверяем баланс
            cursor.execute("SELECT balance FROM Accounts WHERE account_id = ?", (account_id,))
            row = cursor.fetchone()
            if not row:
                print("❌ Счёт не найден!")
                return False

            if row['balance'] > 0:
                print(f"⚠️ На счету осталось {row['balance']} RUB. Сначала снимите все средства!")
                return False

            cursor.execute("UPDATE Accounts SET status = 'closed' WHERE account_id = ?", (account_id,))
            conn.commit()
            print(f"✅ Счёт #{account_id} закрыт")
            return True
    except sqlite3.Error as e:
        print(f"❌ Ошибка закрытия счёта: {e}")
        return False