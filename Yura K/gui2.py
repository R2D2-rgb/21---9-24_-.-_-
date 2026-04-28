import sqlite3

DB = "app.db"

def connect():
    return sqlite3.connect(DB)


def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        balance REAL DEFAULT 0,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        amount REAL,
        type TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------- CLIENTS ----------
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

    cur.execute("SELECT * FROM clients")
    data = cur.fetchall()

    conn.close()
    return data


# ---------- ACCOUNTS ----------
def create_account(client_id, balance):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO accounts(client_id,balance)
    VALUES (?,?)
    """,(client_id,balance))

    conn.commit()
    conn.close()


def get_accounts():
    conn=connect()
    cur=conn.cursor()

    cur.execute(
        "SELECT * FROM accounts"
    )

    rows=cur.fetchall()

    conn.close()
    return rows


# ---------- TRANSACTIONS ----------
def deposit(account_id, amount):
    conn=connect()
    cur=conn.cursor()

    cur.execute("""
    UPDATE accounts
    SET balance = balance + ?
    WHERE id=?
    """,(amount,account_id))

    cur.execute("""
    INSERT INTO transactions(account_id,amount,type)
    VALUES(?,?,?)
    """,(account_id,amount,"deposit"))

    conn.commit()
    conn.close()


def withdraw(account_id, amount):
    conn=connect()
    cur=conn.cursor()

    cur.execute(
        "SELECT balance FROM accounts WHERE id=?",
        (account_id,)
    )

    row=cur.fetchone()

    if not row:
        conn.close()
        return False

    if row[0] < amount:
        conn.close()
        return False


    cur.execute("""
    UPDATE accounts
    SET balance = balance - ?
    WHERE id=?
    """,(amount,account_id))


    cur.execute("""
    INSERT INTO transactions(account_id,amount,type)
    VALUES(?,?,?)
    """,(account_id,amount,"withdraw"))

    conn.commit()
    conn.close()

    return True