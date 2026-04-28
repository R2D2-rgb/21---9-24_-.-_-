import sqlite3

DB_NAME = "app.db"


# -----------------------------
# Подключение
# -----------------------------
def connect():
    return sqlite3.connect(DB_NAME)


# -----------------------------
# Создание таблиц
# -----------------------------
def init_db():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        balance REAL,
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        amount REAL,
        type TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS credits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        amount REAL,
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# КЛИЕНТЫ
# -----------------------------
def add_client(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO clients(name) VALUES(?)",
        (name,)
    )

    conn.commit()
    conn.close()


def get_clients():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM clients"
    )

    data = cur.fetchall()

    conn.close()
    return data


# -----------------------------
# СЧЕТА
# -----------------------------
def create_account(client_id, balance):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO accounts(client_id,balance)
        VALUES(?,?)
        """,
        (client_id,balance)
    )

    conn.commit()
    conn.close()


def get_accounts():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM accounts"
    )

    data = cur.fetchall()

    conn.close()
    return data


# -----------------------------
# ТРАНЗАКЦИИ
# -----------------------------
def deposit(account_id, amount):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE accounts
        SET balance = balance + ?
        WHERE id=?
        """,
        (amount, account_id)
    )

    cur.execute(
        """
        INSERT INTO transactions(account_id,amount,type)
        VALUES(?,?,?)
        """,
        (account_id, amount, "deposit")
    )

    conn.commit()
    conn.close()


def withdraw(account_id, amount):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT balance FROM accounts WHERE id=?",
        (account_id,)
    )

    row = cur.fetchone()

    if not row:
        conn.close()
        return False

    if row[0] < amount:
        conn.close()
        return False

    cur.execute(
        """
        UPDATE accounts
        SET balance=balance-?
        WHERE id=?
        """,
        (amount, account_id)
    )

    cur.execute(
        """
        INSERT INTO transactions(account_id,amount,type)
        VALUES(?,?,?)
        """,
        (account_id, amount, "withdraw")
    )

    conn.commit()
    conn.close()

    return True


# -----------------------------
# КРЕДИТЫ
# -----------------------------
def add_credit(client_id, amount):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO credits(client_id,amount)
        VALUES(?,?)
        """,
        (client_id, amount)
    )

    conn.commit()
    conn.close()


def get_credits():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM credits"
    )

    data = cur.fetchall()

    conn.close()
    return data