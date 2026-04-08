from db import get_connection


def show_all_clients():
    """Отчёт: список всех клиентов с их счетами"""
    query = """
        SELECT 
            c.client_id,
            c.full_name,
            c.phone,
            c.email,
            COUNT(a.account_id) as accounts_count,
            SUM(a.balance) as total_balance,
            COUNT(l.loan_id) as loans_count,
            SUM(l.loan_amount) as total_loans
        FROM Clients c
        LEFT JOIN Accounts a ON c.client_id = a.client_id AND a.status = 'active'
        LEFT JOIN Loans l ON c.client_id = l.client_id AND l.status = 'active'
        GROUP BY c.client_id
        ORDER BY total_balance DESC
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                print("\n📋 Список клиентов пуст.")
                return

            print("\n" + "=" * 110)
            print(
                f"{'ID':<4} | {'ФИО':<25} | {'Телефон':<13} | {'Счетов':<6} | {'Баланс':<15} | {'Кредитов':<8} | {'Сумма кредитов'}")
            print("-" * 110)

            for row in rows:
                print(f"{row['client_id']:<4} | {row['full_name']:<25} | {row['phone']:<13} | "
                      f"{row['accounts_count'] or 0:<6} | {row['total_balance'] or 0:>14.2f} | "
                      f"{row['loans_count'] or 0:<8} | {row['total_loans'] or 0:>14.2f}")
            print("=" * 110)
    except Exception as e:
        print(f"❌ Ошибка отчёта: {e}")


def show_client_accounts(client_id):
    """Отчёт: все счета конкретного клиента"""
    query = """
        SELECT a.account_id, a.account_number, a.account_type, a.balance, a.status, a.opening_date
        FROM Accounts a
        WHERE a.client_id = ?
        ORDER BY a.account_id
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (client_id,))
            rows = cursor.fetchall()

            # Получаем информацию о клиенте
            cursor.execute("SELECT full_name FROM Clients WHERE client_id = ?", (client_id,))
            client = cursor.fetchone()

            if not client:
                print(f"\n❌ Клиент с ID {client_id} не найден!")
                return

            print(f"\n📋 Счета клиента: {client['full_name']}")
            print("=" * 100)
            print(
                f"{'ID':<5} | {'Номер счета':<22} | {'Тип':<10} | {'Баланс':<15} | {'Статус':<10} | {'Дата открытия'}")
            print("-" * 100)

            if not rows:
                print("Нет активных счетов")
            else:
                for row in rows:
                    print(f"{row['account_id']:<5} | {row['account_number']:<22} | {row['account_type']:<10} | "
                          f"{row['balance']:>14.2f} | {row['status']:<10} | {row['opening_date']}")
            print("=" * 100)
    except Exception as e:
        print(f"❌ Ошибка отчёта: {e}")


def show_account_transactions(account_id):
    """Отчёт: история транзакций по счёту"""
    query = """
        SELECT t.transaction_id, t.transaction_type, t.amount, t.transaction_date, t.description
        FROM Transactions t
        WHERE t.account_id = ?
        ORDER BY t.transaction_date DESC
        LIMIT 30
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Получаем информацию о счете
            cursor.execute("""
                SELECT a.account_number, a.account_type, a.balance, c.full_name
                FROM Accounts a
                JOIN Clients c ON a.client_id = c.client_id
                WHERE a.account_id = ?
            """, (account_id,))
            account = cursor.fetchone()

            if not account:
                print(f"\n❌ Счёт с ID {account_id} не найден!")
                return

            print(f"\n📊 История операций по счёту #{account['account_number']}")
            print(f"👤 Владелец: {account['full_name']}")
            print(f"💰 Текущий баланс: {account['balance']:.2f} RUB")
            print("=" * 90)

            cursor.execute(query, (account_id,))
            rows = cursor.fetchall()

            if not rows:
                print("📋 Нет операций по данному счёту")
            else:
                print(f"{'Дата':<20} | {'Тип':<12} | {'Сумма':<12} | {'Описание'}")
                print("-" * 90)
                for row in rows:
                    # Цветовая индикация для разных типов транзакций
                    sign = "+" if row['transaction_type'] == 'deposit' else "-"
                    print(f"{row['transaction_date']:<20} | {row['transaction_type']:<12} | "
                          f"{sign}{row['amount']:>11.2f} | {row['description']}")
            print("=" * 90)
    except Exception as e:
        print(f"❌ Ошибка отчёта: {e}")


def show_all_loans():
    """Отчёт: все активные кредиты"""
    query = """
        SELECT 
            l.loan_id,
            c.full_name,
            l.loan_amount,
            l.interest_rate,
            l.term_months,
            l.issue_date,
            l.status,
            a.account_number
        FROM Loans l
        JOIN Clients c ON l.client_id = c.client_id
        LEFT JOIN Accounts a ON l.account_id = a.account_id
        WHERE l.status = 'active'
        ORDER BY l.loan_amount DESC
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                print("\n📋 Активных кредитов нет.")
                return

            print("\n" + "🏦" * 30)
            print("                    АКТИВНЫЕ КРЕДИТЫ")
            print("🏦" * 30)
            print(f"{'ID':<4} | {'Клиент':<25} | {'Сумма':<12} | {'Ставка':<7} | {'Срок':<8} | {'Дата выдачи'}")
            print("-" * 80)

            total_loans = 0
            for row in rows:
                print(f"{row['loan_id']:<4} | {row['full_name']:<25} | {row['loan_amount']:>11.2f} | "
                      f"{row['interest_rate']:>5.1f}% | {row['term_months']:>3} мес | {row['issue_date']}")
                total_loans += row['loan_amount']

            print("-" * 80)
            print(f"📊 Общая сумма выданных кредитов: {total_loans:,.2f} RUB")
            print("🏦" * 30)
    except Exception as e:
        print(f"❌ Ошибка отчёта: {e}")


def get_bank_summary():
    """Отчёт: финансовая сводка банка (предметная логика)"""
    queries = {
        'total_clients': "SELECT COUNT(*) as count FROM Clients",
        'total_accounts': "SELECT COUNT(*) as count FROM Accounts WHERE status = 'active'",
        'total_balance': "SELECT SUM(balance) as total FROM Accounts WHERE status = 'active'",
        'total_loans': "SELECT SUM(loan_amount) as total FROM Loans WHERE status = 'active'",
        'total_transactions_today': """
            SELECT COUNT(*) as count, SUM(amount) as total 
            FROM Transactions 
            WHERE date(transaction_date) = date('now')
        """,
        'avg_balance': "SELECT AVG(balance) as avg FROM Accounts WHERE status = 'active'"
    }

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Собираем статистику
            stats = {}
            for key, query in queries.items():
                cursor.execute(query)
                stats[key] = cursor.fetchone()

            print("\n" + "🏦" * 35)
            print("                    БАНКОВСКАЯ СВОДКА")
            print("🏦" * 35)
            print(f"👥 Всего клиентов:                 {stats['total_clients']['count']}")
            print(f"💳 Активных счетов:                {stats['total_accounts']['count']}")
            print(f"💰 Общий баланс всех счетов:       {stats['total_balance']['total'] or 0:,.2f} RUB")
            print(f"📊 Средний баланс по счетам:       {stats['avg_balance']['avg'] or 0:,.2f} RUB")
            print(f"🏦 Общая сумма активных кредитов:   {stats['total_loans']['total'] or 0:,.2f} RUB")
            print(f"📈 Транзакций сегодня:             {stats['total_transactions_today']['count'] or 0}")
            print(f"💸 Оборот сегодня:                 {stats['total_transactions_today']['total'] or 0:,.2f} RUB")
            print("🏦" * 35)

            # Дополнительный анализ: топ-5 клиентов по балансу
            cursor.execute("""
                SELECT c.full_name, SUM(a.balance) as total_balance
                FROM Clients c
                JOIN Accounts a ON c.client_id = a.client_id
                WHERE a.status = 'active'
                GROUP BY c.client_id
                ORDER BY total_balance DESC
                LIMIT 5
            """)
            top_clients = cursor.fetchall()

            if top_clients:
                print("\n🌟 ТОП-5 КЛИЕНТОВ ПО БАЛАНСУ:")
                print("-" * 50)
                for i, client in enumerate(top_clients, 1):
                    print(f"{i}. {client['full_name']:<30} {client['total_balance']:>15,.2f} RUB")
            print("🏦" * 35)
    except Exception as e:
        print(f"❌ Ошибка отчёта: {e}")