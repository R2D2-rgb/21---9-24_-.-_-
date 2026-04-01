import tkinter as tk
from tkinter import messagebox

# ===== ДАННЫЕ (временно) =====
clients = []
accounts = []

# ===== ГЛАВНОЕ ОКНО =====
root = tk.Tk()
root.title("Банк")
root.geometry("400x400")


# ===== ФУНКЦИИ =====

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu():
    clear_window()

    tk.Label(root, text="БАНКОВСКАЯ СИСТЕМА", font=("Arial", 14)).pack(pady=20)

    tk.Button(root, text="Клиенты", width=20, command=clients_menu).pack(pady=5)
    tk.Button(root, text="Счета", width=20, command=accounts_menu).pack(pady=5)
    tk.Button(root, text="Выход", width=20, command=root.quit).pack(pady=20)


# ===== КЛИЕНТЫ =====
def clients_menu():
    clear_window()

    tk.Label(root, text="Клиенты", font=("Arial", 14)).pack(pady=10)

    entry = tk.Entry(root)
    entry.pack(pady=5)

    listbox = tk.Listbox(root)
    listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    def update_list():
        listbox.delete(0, tk.END)
        for c in clients:
            listbox.insert(tk.END, f"{c['id']}. {c['name']}")

    def add_client():
        name = entry.get()
        if name == "":
            messagebox.showerror("Ошибка", "Введите имя")
            return

        client = {"id": len(clients) + 1, "name": name}
        clients.append(client)

        entry.delete(0, tk.END)
        update_list()

    tk.Button(root, text="Добавить", command=add_client).pack(pady=5)
    tk.Button(root, text="Назад", command=main_menu).pack(pady=5)

    update_list()


# ===== СЧЕТА =====
def accounts_menu():
    clear_window()

    tk.Label(root, text="Счета", font=("Arial", 14)).pack(pady=10)

    entry_client = tk.Entry(root)
    entry_client.insert(0, "ID клиента")
    entry_client.pack(pady=5)

    entry_balance = tk.Entry(root)
    entry_balance.insert(0, "Баланс")
    entry_balance.pack(pady=5)

    listbox = tk.Listbox(root)
    listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    def update_list():
        listbox.delete(0, tk.END)
        for acc in accounts:
            listbox.insert(
                tk.END,
                f"ID:{acc['id']} | Клиент:{acc['client_id']} | Баланс:{acc['balance']}"
            )

    def create_account():
        try:
            client_id = int(entry_client.get())
            balance = float(entry_balance.get())

            acc = {
                "id": len(accounts) + 1,
                "client_id": client_id,
                "balance": balance
            }

            accounts.append(acc)
            update_list()

        except:
            messagebox.showerror("Ошибка", "Неверный ввод")

    tk.Button(root, text="Создать счет", command=create_account).pack(pady=5)
    tk.Button(root, text="Назад", command=main_menu).pack(pady=5)

    update_list()


# ===== ТРАНЗАКЦИИ =====
def transactions_menu():
    clear_window()

    tk.Label(root, text="Транзакции", font=("Arial", 14)).pack(pady=10)

    entry_acc = tk.Entry(root)
    entry_acc.insert(0, "ID счета")
    entry_acc.pack(pady=5)

    entry_amount = tk.Entry(root)
    entry_amount.insert(0, "Сумма")
    entry_amount.pack(pady=5)

    def deposit():
        try:
            acc_id = int(entry_acc.get())
            amount = float(entry_amount.get())

            for acc in accounts:
                if acc["id"] == acc_id:
                    acc["balance"] += amount
                    messagebox.showinfo("Успех", "Пополнение выполнено")
                    return

            messagebox.showerror("Ошибка", "Счет не найден")

        except:
            messagebox.showerror("Ошибка", "Неверный ввод")

    def withdraw():
        try:
            acc_id = int(entry_acc.get())
            amount = float(entry_amount.get())

            for acc in accounts:
                if acc["id"] == acc_id:
                    if acc["balance"] >= amount:
                        acc["balance"] -= amount
                        messagebox.showinfo("Успех", "Снятие выполнено")
                    else:
                        messagebox.showerror("Ошибка", "Недостаточно средств")
                    return

            messagebox.showerror("Ошибка", "Счет не найден")

        except:
            messagebox.showerror("Ошибка", "Неверный ввод")

    tk.Button(root, text="Пополнить", command=deposit).pack(pady=5)
    tk.Button(root, text="Снять", command=withdraw).pack(pady=5)
    tk.Button(root, text="Назад", command=main_menu).pack(pady=10)


# ===== ЗАПУСК =====
main_menu()
root.mainloop()