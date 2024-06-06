import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import bcrypt
import ttkbootstrap as ttkb
from datetime import datetime
from dateutil import parser
def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-1EP0LPKF\\SQLEXPRESS;"  # Имя сервера и экземпляра
        "DATABASE=Nikita_database;"  # Имя базы данных
        "UID=nikita_user;"  # Имя нового пользователя
        "PWD=NewStrongPassword123"  # Пароль нового пользователя
    )
    return pyodbc.connect(conn_str)

def login():
    username = entry_username.get()
    password = entry_password.get().encode('utf-8')

    # Проверка логина и пароля
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Password, Role FROM Users WHERE Username=?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row and bcrypt.checkpw(password, row[0].encode('utf-8')):
        role = row[1]
        if role == "client":
            open_client_window()
        elif role == "admin":
            open_admin_window()
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

def register():
    username = entry_username.get()
    password = entry_password.get().encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (Username, Password, Role) VALUES (?, ?, ?)", (username, hashed, "client"))
    conn.commit()
    conn.close()
    messagebox.showinfo("Успех", "Пользователь зарегистрирован")


def open_client_window():
    client_window = tk.Toplevel(root)
    client_window.title("Клиент")

    frame_form = ttk.Frame(client_window, padding="10")
    frame_form.grid(row=0, column=0, sticky=tk.W)

    # Поля ввода
    ttk.Label(frame_form, text="Фамилия").grid(row=0, column=0, padx=5, pady=5)
    entry_last_name = ttk.Entry(frame_form)
    entry_last_name.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Имя").grid(row=1, column=0, padx=5, pady=5)
    entry_first_name = ttk.Entry(frame_form)
    entry_first_name.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Отчество").grid(row=2, column=0, padx=5, pady=5)
    entry_middle_name = ttk.Entry(frame_form)
    entry_middle_name.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Дата начала аренды").grid(row=3, column=0, padx=5, pady=5)
    entry_start_date = ttk.Entry(frame_form)
    entry_start_date.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Дата окончания аренды").grid(row=4, column=0, padx=5, pady=5)
    entry_end_date = ttk.Entry(frame_form)
    entry_end_date.grid(row=4, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Марка").grid(row=5, column=0, padx=5, pady=5)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Марка FROM Автомобиль")
    marks = [row[0] for row in cursor.fetchall()]
    combo_mark = ttk.Combobox(frame_form, values=marks, state="readonly")
    combo_mark.grid(row=5, column=1, padx=5, pady=5)
    conn.close()

    ttk.Label(frame_form, text="Год выпуска").grid(row=6, column=0, padx=5, pady=5)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT ГодВыпуска FROM Автомобиль")
    years = [row[0] for row in cursor.fetchall()]
    combo_year = ttk.Combobox(frame_form, values=years, state="readonly")
    combo_year.grid(row=6, column=1, padx=5, pady=5)
    conn.close()

    # Выпадающий список для VIN
    ttk.Label(frame_form, text="VIN").grid(row=7, column=0, padx=5, pady=5)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT VIN FROM Автомобиль")
    vin_values = [row[0] for row in cursor.fetchall()]
    combo_vin = ttk.Combobox(frame_form, values=vin_values, state="readonly")
    combo_vin.grid(row=7, column=1, padx=5, pady=5)
    conn.close()

    # Выпадающий список для типа кузова
    ttk.Label(frame_form, text="Тип кузова").grid(row=8, column=0, padx=5, pady=5)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT ТипКузова FROM Автомобиль")
    body_type_values = [row[0] for row in cursor.fetchall()]
    combo_body_type = ttk.Combobox(frame_form, values=body_type_values, state="readonly")
    combo_body_type.grid(row=8, column=1, padx=5, pady=5)
    conn.close()

    # Выпадающий список для объема двигателя
    ttk.Label(frame_form, text="Объем двигателя").grid(row=9, column=0, padx=5, pady=5)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT ОбъемДвигателя FROM Автомобиль")
    engine_volume_values = [row[0] for row in cursor.fetchall()]
    combo_engine_volume = ttk.Combobox(frame_form, values=engine_volume_values, state="readonly")
    combo_engine_volume.grid(row=9, column=1, padx=5, pady=5)
    conn.close()

    # Выпадающий список для цвета кузова
    ttk.Label(frame_form, text="Цвет кузова").grid(row=10, column=0, padx=5, pady=5)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT ЦветКузова FROM Автомобиль")
    color_values = [row[0] for row in cursor.fetchall()]
    combo_color = ttk.Combobox(frame_form, values=color_values, state="readonly")
    combo_color.grid(row=10, column=1, padx=5, pady=5)
    conn.close()

    # Поле для отображения стоимости
    ttk.Label(frame_form, text="Стоимость").grid(row=11, column=0, padx=5, pady=5)
    label_cost = ttk.Label(frame_form, text="")
    label_cost.grid(row=11, column=1, padx=5, pady=5)

    # Функция для расчета стоимости
    def update_cost():
        try:
            start_date_str = entry_start_date.get()
            end_date_str = entry_end_date.get()
            mark = combo_mark.get()

            if not start_date_str.strip() or not end_date_str.strip():
                return

            try:
                start_date = parser.parse(start_date_str.strip())
                end_date = parser.parse(end_date_str.strip())
            except ValueError:
                return

            if mark and start_date and end_date:
                duration = abs((end_date - start_date).days) + 1  # Добавляем 1, чтобы включить последний день
                cost = calculate_cost(mark, duration)
                label_cost.config(text=str(cost))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    combo_mark.bind("<<ComboboxSelected>>", lambda _: update_cost())
    entry_start_date.bind("<FocusOut>", lambda _: update_cost())
    entry_end_date.bind("<FocusOut>", lambda _: update_cost())

    # Кнопка для отправки данных
    ttk.Button(frame_form, text="Отправить", command=lambda: submit_client_form(
        entry_last_name, entry_first_name, entry_middle_name, entry_start_date, entry_end_date,
        combo_mark, combo_year, combo_vin, combo_body_type, combo_engine_volume, combo_color, label_cost
    )).grid(row=12, columnspan=2, padx=5, pady=5)

    # Кнопка для описания конфликтной ситуации
    ttk.Button(frame_form, text="Описать конфликтную ситуацию", command=open_conflict_window).grid(row=13, columnspan=2, padx=5, pady=5)


def submit_client_form(entry_last_name, entry_first_name, entry_middle_name, entry_start_date, entry_end_date,
                       combo_mark, combo_year, combo_vin, combo_body_type, combo_engine_volume, combo_color, label_cost):
    last_name = entry_last_name.get()
    first_name = entry_first_name.get()
    middle_name = entry_middle_name.get()
    start_date_str = entry_start_date.get()
    end_date_str = entry_end_date.get()
    mark = combo_mark.get()
    year = combo_year.get()
    vin = combo_vin.get()
    body_type = combo_body_type.get()
    engine_volume = combo_engine_volume.get()
    color = combo_color.get()
    cost = label_cost.cget("text")

    if not (last_name and first_name and middle_name and start_date_str and end_date_str and mark and year and vin and body_type and engine_volume and color and cost):
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
        return

    try:
        # Проверка и преобразование даты
        try:
            start_date = parser.parse(start_date_str.strip())
            end_date = parser.parse(end_date_str.strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите даты в корректном формате")
            return

        # Пересчитываем стоимость на основе даты
        duration = abs((end_date - start_date).days) + 1
        cost = calculate_cost(mark, duration)
        label_cost.config(text=str(cost))

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Арендатор (Фамилия, Имя, Отчество) VALUES (?, ?, ?)",
                       (last_name, first_name, middle_name))
        cursor.execute("INSERT INTO Аренда (АвтомобильID, АрендаторID, ДатаНачалаАренды, ДатаОкончанияАренды, СтоимостьАренды) VALUES ((SELECT АвтомобильID FROM Автомобиль WHERE VIN=?), (SELECT MAX(АрендаторID) FROM Арендатор), ?, ?, ?)",
                       (vin, start_date_str, end_date_str, cost))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", "Данные успешно отправлены")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


def calculate_cost(mark, duration):
    base_cost_per_day = {
        "Toyota": 1000,
        "Nissan X-Trail": 1200,
        "Honda Accord": 1300,
        "Hyundai Tucson": 1500
    }
    cost_per_day = base_cost_per_day.get(mark, 1000)
    total_cost = cost_per_day * duration
    return total_cost

def open_conflict_window():
    conflict_window = tk.Toplevel(root)
    conflict_window.title("Конфликтная ситуация")

    frame_conflict = ttk.Frame(conflict_window, padding="10")
    frame_conflict.grid(row=0, column=0, sticky=tk.W)

    ttk.Label(frame_conflict, text="Описание конфликта").grid(row=0, column=0, padx=5, pady=5)
    entry_description = ttk.Entry(frame_conflict)
    entry_description.grid(row=0, column=1, padx=5, pady=5)

    # Кнопка для отправки конфликта
    ttk.Button(frame_conflict, text="Отправить", command=lambda: submit_conflict_form(entry_description)).grid(row=1, columnspan=2, padx=5, pady=5)


def submit_conflict_form(entry_description):
    description = entry_description.get()
    if not description:
        messagebox.showerror("Ошибка", "Описание конфликта не может быть пустым")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Получите ID последнего автомобиля, арендованного текущим пользователем
        cursor.execute("SELECT TOP 1 АвтомобильID FROM Аренда ORDER BY АрендаID DESC")
        car_id = cursor.fetchone()

        if not car_id:
            messagebox.showerror("Ошибка", "Не удалось определить ID автомобиля")
            return

        cursor.execute("INSERT INTO КонфликтныеСитуации (АвтомобильID, ОписаниеКонфликта) VALUES (?, ?)",
                       (car_id[0], description))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", "Конфликтная ситуация успешно добавлена")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))



def get_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CONCAT(Фамилия, ' ', Имя, ' ', Отчество) AS ПолноеИмя FROM Сотрудник")
    employees = [row[0] for row in cursor.fetchall()]
    conn.close()
    return employees


# Функция для открытия окна администратора
def open_admin_window():
    admin_window = tk.Toplevel()
    admin_window.title("Администратор")

    frame_admin = ttk.Frame(admin_window, padding="10")
    frame_admin.grid(row=0, column=0, sticky=tk.W)

    columns = ("ID аренды", "Фамилия", "Имя", "Отчество", "Автомобиль", "Дата начала аренды", "Дата окончания аренды", "Стоимость аренды", "Дата оформления договора", "Номер договора", "Сотрудник")
    tree_orders = ttk.Treeview(frame_admin, columns=columns, show="headings")

    for col in columns:
        tree_orders.heading(col, text=col)
        tree_orders.column(col, width=100)

    tree_orders.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

    ttk.Label(frame_admin, text="Номер договора").grid(row=1, column=0, padx=5, pady=5)
    entry_contract_number = ttk.Entry(frame_admin)
    entry_contract_number.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_admin, text="Сотрудник").grid(row=2, column=0, padx=5, pady=5)
    employee_values = get_employees()
    combo_employee = ttk.Combobox(frame_admin, values=employee_values)
    combo_employee.grid(row=2, column=1, padx=5, pady=5)

    # Кнопка для назначения сотрудника
    ttk.Button(frame_admin, text="Назначить сотрудника", command=lambda: assign_employee(tree_orders, combo_employee, entry_contract_number)).grid(row=3, column=0, padx=5, pady=5, columnspan=2)

    # Кнопка для загрузки данных
    ttk.Button(frame_admin, text="Загрузить данные", command=lambda: load_orders(tree_orders)).grid(row=4, column=0, padx=5, pady=5, columnspan=2)

def assign_employee(tree, combo_employee, entry_contract_number):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите запись для назначения сотрудника")
        return

    employee = combo_employee.get()
    contract_number = entry_contract_number.get()

    if not (employee and contract_number):
        messagebox.showerror("Ошибка", "Заполните все поля")
        return

    item = tree.item(selected_item)
    order_id = item['values'][0]

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Аренда 
            SET СотрудникID = (SELECT СотрудникID FROM Сотрудник WHERE CONCAT(Фамилия, ' ', Имя, ' ', Отчество) = ?),
                НомерДоговора = ?
            WHERE АрендаID = ?
        """, (employee, contract_number, order_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", "Сотрудник назначен")
        load_orders(tree)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))




def load_orders(tree_orders):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        a.АрендаID,
        ar.Фамилия,
        ar.Имя,
        ar.Отчество,
        av.Марка,
        a.ДатаНачалаАренды,
        a.ДатаОкончанияАренды,
        a.СтоимостьАренды,
        a.ДатаОформленияДоговора,
        a.НомерДоговора,
        CONCAT(s.Фамилия, ' ', s.Имя, ' ', s.Отчество) AS Сотрудник
    FROM Аренда a
    JOIN Арендатор ar ON a.АрендаторID = ar.АрендаторID
    JOIN Автомобиль av ON a.АвтомобильID = av.АвтомобильID
    LEFT JOIN Сотрудник s ON a.СотрудникID = s.СотрудникID
    """)
    rows = cursor.fetchall()
    for row in rows:
        row = list(row)
        row[5] = row[5].strftime('%d.%m.%Y')
        row[6] = row[6].strftime('%d.%m.%Y')
        row[8] = row[8].strftime('%d.%m.%Y') if row[8] else ''
        tree_orders.insert("", "end", values=row)
    conn.close()


# Функция для назначения сотрудника
def assign_employee(tree_orders, combo_employee, entry_contract_number):
    selected_item = tree_orders.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите аренду для назначения сотрудника.")
        return

    contract_number = entry_contract_number.get()
    employee = combo_employee.get()

    if not contract_number or not employee:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
        return

    employee_id = get_employee_id(employee)
    rental_id = tree_orders.item(selected_item[0], "values")[0]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Аренда SET СотрудникID=?, НомерДоговора=? WHERE АрендаID=?", (employee_id, contract_number, rental_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Успех", "Сотрудник назначен.")
    load_orders(tree_orders)

def get_employee_id(full_name):
    last_name, first_name, middle_name = full_name.split()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT СотрудникID FROM Сотрудник WHERE Фамилия=? AND Имя=? AND Отчество=?", (last_name, first_name, middle_name))
    employee_id = cursor.fetchone()[0]
    conn.close()
    return employee_id
# Создание главного окна
root = tk.Tk()
root.title("Вход")


# Фрейм для формы входа
frame_login = ttk.Frame(root, padding="10")
frame_login.grid(row=0, column=0, sticky=tk.W)

# Поля ввода логина и пароля
ttk.Label(frame_login, text="Имя пользователя").grid(row=0, column=0, padx=5, pady=5)
entry_username = ttk.Entry(frame_login)
entry_username.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_login, text="Пароль").grid(row=1, column=0, padx=5, pady=5)
entry_password = ttk.Entry(frame_login, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=5)

# Кнопки для входа и регистрации
ttk.Button(frame_login, text="Войти", command=login).grid(row=2, columnspan=2, padx=5, pady=5)
ttk.Button(frame_login, text="Регистрация", command=register).grid(row=3, columnspan=2, padx=5, pady=5)


root.mainloop()
