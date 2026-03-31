# interface.py

# ===== ВРЕМЕННЫЕ ДАННЫЕ (вместо БД) =====
clients = []
accounts = []
transactions = []
credits = []


# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu():
    print("\n=== БАНКОВСКАЯ СИСТЕМА ===")
    print("1. Клиенты")
    print("2. Счета")
    print("3. Транзакции")
    print("4. Кредиты")
    print("0. Выход")
    return input("Выберите: ")


# ===== КЛИЕНТЫ =====
def clients_menu():
    while True:
        print("\n--- Клиенты ---")
        print("1. Добавить клиента")
        print("2. Показать клиентов")
        print("0. Назад")

        choice = input(">> ")

        if choice == "1":
            add_client()
        elif choice == "2":
            show_clients()
        elif choice == "0":
            break
        else:
            print("Ошибка!")


def add_client():
    name = input("Имя клиента: ")
    client_id = len(clients) + 1

    client = {
        "id": client_id,
        "name": name
    }

    clients.append(client)
    print("Клиент добавлен!")


def show_clients():
    if not clients:
        print("Нет клиентов")
        return

    for c in clients:
        print(f"{c['id']}. {c['name']}")


# ===== СЧЕТА =====
def accounts_menu():
    while True:
        print("\n--- Счета ---")
        print("1. Открыть счет")
        print("2. Показать счета")
        print("0. Назад")

        choice = input(">> ")

        if choice == "1":
            create_account()
        elif choice == "2":
            show_accounts()
        elif choice == "0":
            break
        else:
            print("Ошибка!")


def create_account():
    try:
        client_id = int(input("ID клиента: "))
        balance = float(input("Начальный баланс: "))

        account_id = len(accounts) + 1

        account = {
            "id": account_id,
            "client_id": client_id,
            "balance": balance
        }

        accounts.append(account)
        print("Счет создан!")

    except ValueError:
        print("Ошибка ввода!")


def show_accounts():
    if not accounts:
        print("Нет счетов")
        return

    for acc in accounts:
        print(acc)


# ===== ТРАНЗАКЦИИ =====
def transactions_menu():
    while True:
        print("\n--- Транзакции ---")
        print("1. Пополнение")
        print("2. Снятие")
        print("0. Назад")

        choice = input(">> ")

        if choice == "1":
            deposit()
        elif choice == "2":
            withdraw()
        elif choice == "0":
            break
        else:
            print("Ошибка!")


def deposit():
    try:
        acc_id = int(input("ID счета: "))
        amount = float(input("Сумма: "))

        for acc in accounts:
            if acc["id"] == acc_id:
                acc["balance"] += amount
                print("Пополнение успешно!")
                return

        print("Счет не найден!")

    except ValueError:
        print("Ошибка!")


def withdraw():
    try:
        acc_id = int(input("ID счета: "))
        amount = float(input("Сумма: "))

        for acc in accounts:
            if acc["id"] == acc_id:
                if acc["balance"] >= amount:
                    acc["balance"] -= amount
                    print("Снятие успешно!")
                else:
                    print("Недостаточно средств!")
                return

        print("Счет не найден!")

    except ValueError:
        print("Ошибка!")


# ===== КРЕДИТЫ =====
def credits_menu():
    while True:
        print("\n--- Кредиты ---")
        print("1. Выдать кредит")
        print("2. Показать кредиты")
        print("0. Назад")

        choice = input(">> ")

        if choice == "1":
            create_credit()
        elif choice == "2":
            show_credits()
        elif choice == "0":
            break
        else:
            print("Ошибка!")


def create_credit():
    try:
        client_id = int(input("ID клиента: "))
        amount = float(input("Сумма кредита: "))

        credit_id = len(credits) + 1

        credit = {
            "id": credit_id,
            "client_id": client_id,
            "amount": amount
        }

        credits.append(credit)
        print("Кредит выдан!")

    except ValueError:
        print("Ошибка!")


def show_credits():
    if not credits:
        print("Нет кредитов")
        return

    for cr in credits:
        print(cr)


# ===== ЗАПУСК =====
def run():
    while True:
        choice = main_menu()

        if choice == "1":
            clients_menu()
        elif choice == "2":
            accounts_menu()
        elif choice == "3":
            transactions_menu()
        elif choice == "4":
            credits_menu()
        elif choice == "0":
            print("Выход...")
            break
        else:
            print("Ошибка!")


if __name__ == "__main__":
    run()