import tkinter as tk
from tkinter import messagebox

# ===== ДАННЫЕ (временно) =====
clients = []
accounts = []

# ===== ГЛАВНОЕ ОКНО =====
root = tk.Tk()
root.title("Банк")
root.geometry("400x400")

# ===== АНИМАЦИИ =====
root.attributes("-alpha", 0.0)

def fade_in(step=0.1):
    alpha = root.attributes("-alpha")
    if alpha < 1:
        alpha += step
        root.attributes("-alpha", alpha)
        root.after(15, fade_in)

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

def animate_switch(new_screen_func, step=0.1):
    def fade_out():
        alpha = root.attributes("-alpha")
        if alpha > 0:
            alpha -= step
            root.attributes("-alpha", alpha)
            root.after(10, fade_out)
        else:
            clear_window()
            new_screen_func()
            fade_in()
    fade_out()

# ===== ЭФФЕКТЫ КНОПОК =====
def on_enter(e):
    e.widget["background"] = "#d1e7dd"

def on_leave(e):
    e.widget["background"] = "SystemButtonFace"

def create_button(text, command, bottom=False, danger=False):
    btn = tk.Button(root, text=text, width=20, command=command)

    if bottom:
        btn.pack(side="bottom", pady=10)
    else:
        btn.pack(pady=5)

    if danger:
        btn.bind("<Enter>", lambda e: e.widget.config(background="#ff4d4d"))
        btn.bind("<Leave>", lambda e: e.widget.config(background="SystemButtonFace"))
    else:
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    return btn

# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu():
    clear_window()

    tk.Label(root, text="БАНКОВСКАЯ СИСТЕМА", font=("Arial", 14)).pack(pady=20)

    create_button("Клиенты", lambda: animate_switch(clients_menu))
    create_button("Счета", lambda: animate_switch(accounts_menu))
    create_button("Транзакции", lambda: animate_switch(transactions_menu))

    create_button("Выход", root.quit, bottom=True, danger=True)

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

    create_button("Добавить", add_client)
    create_button("Назад", lambda: animate_switch(main_menu), bottom=True)

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

    create_button("Создать счет", create_account)
    create_button("Назад", lambda: animate_switch(main_menu), bottom=True)

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

    create_button("Пополнить", deposit)
    create_button("Снять", withdraw)
    create_button("Назад", lambda: animate_switch(main_menu), bottom=True)

# ===== ЗАПУСК =====
main_menu()
fade_in()
root.mainloop()
