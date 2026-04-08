import sys
from db import init_db
from services import (
    add_client, open_account, perform_transaction,
    take_loan, close_account
)
from reports import (
    show_all_clients, show_client_accounts,
    show_account_transactions, show_all_loans, get_bank_summary
)


def print_menu():
    print("\n" + "=" * 50)
    print("   🏦 БАНКОВСКАЯ СИСТЕМА v2.0 🏦")
    print("=" * 50)
    print("\n📋 ГЛАВНОЕ МЕНЮ:")
    print("─" * 50)
    print("👥 УПРАВЛЕНИЕ КЛИЕНТАМИ:")
    print("  1. 👥 Показать всех клиентов")
    print("  2. ➕ Добавить нового клиента")
    print("  3. 💳 Показать счета клиента")
    print("\n💳 УПРАВЛЕНИЕ СЧЕТАМИ:")
    print("  4. 🆕 Открыть счёт")
    print("  5. 🔒 Закрыть счёт")
    print("  6. 📊 История операций по счёту")
    print("\n💰 ОПЕРАЦИИ:")
    print("  7. 💸 Пополнение счёта")
    print("  8. 💰 Снятие средств")
    print("  9. 🔄 Перевод между счетами")
    print("\n🏦 КРЕДИТЫ:")
    print("  10. 📝 Оформить кредит")
    print("  11. 📋 Все активные кредиты")
    print("\n📊 ОТЧЁТЫ:")
    print("  12. 📈 Банковская сводка")
    print("\n" + "─" * 50)
    print("  0. 🚪 Выход")
    print("=" * 50)


def main():
    # Инициализация базы данных
    init_db()

    while True:
        print_menu()
        choice = input("\n👉 Ваш выбор: ").strip()

        if choice == "1":
            show_all_clients()

        elif choice == "2":
            print("\n--- Добавление нового клиента ---")
            full_name = input("ФИО: ").strip()
            phone = input("Телефон: ").strip()
            email = input("Email: ").strip()
            address = input("Адрес: ").strip()
            passport_data = input("Паспортные данные: ").strip()

            if full_name and phone and passport_data:
                add_client(full_name, phone, email, address, passport_data)
            else:
                print("❌ ФИО, телефон и паспорт обязательны!")

        elif choice == "3":
            print("\n--- Показать счета клиента ---")
            try:
                client_id = int(input("ID клиента: "))
                show_client_accounts(client_id)
            except ValueError:
                print("❌ Ошибка: введите корректный ID!")

        elif choice == "4":
            print("\n--- Открытие счёта ---")
            try:
                client_id = int(input("ID клиента: "))
                print("Типы счетов: debit, credit, deposit")
                account_type = input("Тип счёта: ").strip().lower()
                if account_type not in ['debit', 'credit', 'deposit']:
                    print("❌ Неверный тип счёта!")
                    continue
                initial_balance = float(input("Начальный баланс: ") or "0")
                open_account(client_id, account_type, initial_balance)
            except ValueError:
                print("❌ Ошибка: введите корректные числа!")

        elif choice == "5":
            print("\n--- Закрытие счёта ---")
            try:
                account_id = int(input("ID счёта: "))
                close_account(account_id)
            except ValueError:
                print("❌ Ошибка: введите корректный ID!")

        elif choice == "6":
            print("\n--- История операций ---")
            try:
                account_id = int(input("ID счёта: "))
                show_account_transactions(account_id)
            except ValueError:
                print("❌ Ошибка: введите корректный ID счёта!")

        elif choice == "7":
            print("\n--- Пополнение счёта ---")
            try:
                account_id = int(input("ID счёта: "))
                amount = float(input("Сумма пополнения: "))
                perform_transaction(account_id, 'deposit', amount, "Пополнение счёта")
            except ValueError:
                print("❌ Ошибка: введите корректные числа!")

        elif choice == "8":
            print("\n--- Снятие средств ---")
            try:
                account_id = int(input("ID счёта: "))
                amount = float(input("Сумма снятия: "))
                perform_transaction(account_id, 'withdrawal', amount, "Снятие наличных")
            except ValueError:
                print("❌ Ошибка: введите корректные числа!")

        elif choice == "9":
            print("\n--- Перевод между счетами ---")
            try:
                from_account = int(input("Счёт ОТКУДА (ID): "))
                to_account = int(input("Счёт КУДА (ID): "))
                amount = float(input("Сумма перевода: "))

                # Снимаем с первого счёта
                if perform_transaction(from_account, 'withdrawal', amount, f"Перевод на счёт {to_account}"):
                    # Зачисляем на второй счёт
                    perform_transaction(to_account, 'deposit', amount, f"Перевод со счёта {from_account}")
            except ValueError:
                print("❌ Ошибка: введите корректные числа!")

        elif choice == "10":
            print("\n--- Оформление кредита ---")
            try:
                client_id = int(input("ID клиента: "))
                account_id = int(input("ID счёта для зачисления: "))
                loan_amount = float(input("Сумма кредита: "))
                interest_rate = float(input("Процентная ставка (%): "))
                term_months = int(input("Срок (месяцев): "))
                take_loan(client_id, account_id, loan_amount, interest_rate, term_months)
            except ValueError:
                print("❌ Ошибка: введите корректные числа!")

        elif choice == "11":
            show_all_loans()

        elif choice == "12":
            get_bank_summary()

        elif choice == "0":
            print("\n👋 До свидания! Спасибо, что пользуетесь нашим банком!")
            print("📊 Итоговая статистика сессии:")
            get_bank_summary()
            sys.exit()

        else:
            print("❌ Неверный выбор! Введите число от 0 до 12.")

        input("\n🔹 Нажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Программа прервана. До свидания!")