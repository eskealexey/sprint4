"""
Журнал тренировок
"""
import tkinter as tk
from tkinter import ttk, Toplevel, messagebox, Button
import re
import json
from datetime import datetime
from tkinter.constants import RIGHT, BOTTOM

# Файл для сохранения данных
data_file = 'training_log.json'

def load_data():
    """Загрузка данных о тренировках из файла."""
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """Сохранение данных о тренировках в файл."""
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

class TrainingLogApp:
    def __init__(self, root):
        self.root = root
        root.title("Дневник тренировок")
        self.create_widgets()

    def create_widgets(self):
        """Создание виджетов."""
        # Виджеты для ввода данных
        self.exercise_label = ttk.Label(self.root, text="Упражнение:")
        self.exercise_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.exercise_entry = ttk.Entry(self.root)
        self.exercise_entry.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        self.weight_label = ttk.Label(self.root, text="Вес:")
        self.weight_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        self.repetitions_label = ttk.Label(self.root, text="Повторения:")
        self.repetitions_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.repetitions_entry = ttk.Entry(self.root)
        self.repetitions_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        self.add_button = ttk.Button(self.root, text="Добавить запись", command=self.add_entry)
        self.add_button.grid(column=0, row=3, columnspan=2, pady=10)

        self.view_button = ttk.Button(self.root, text="Просмотреть записи", command=self.view_records)
        self.view_button.grid(column=0, row=4, columnspan=2, pady=10)

    def add_entry(self):
        """Добавление записи."""
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exercise = self.exercise_entry.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()

        if not (exercise and weight and repetitions):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        entry = {
            'date': date,
            'exercise': exercise,
            'weight': weight,
            'repetitions': repetitions
        }

        data = load_data()
        data.append(entry)
        save_data(data)

        # Очистка полей ввода после добавления
        self.exercise_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.repetitions_entry.delete(0, tk.END)
        messagebox.showinfo("Успешно", "Запись успешно добавлена!")

    def view_records(self, up=None):
        """Просмотреть записи."""
        if up:
            data = up
        else:
            data = load_data()
        records_window = Toplevel(self.root)
        records_window.title("Записи тренировок")
        place_ = ttk.Frame(records_window, padding=10,relief=tk.RIDGE)
        place_.pack()
        tree = ttk.Treeview(place_, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")
        scrollbar = ttk.Scrollbar(place_, orient="vertical", command=tree.yview)
        scrollbar.pack(side=RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)#
        btn = ttk.Button(records_window, text="Закрыть", command=records_window.destroy)
        btn.pack(side=tk.BOTTOM, pady=10)

        frame1 = ttk.Frame(records_window, borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        frame1.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.NW)

        lbl_select_date = ttk.Label(frame1, text="Введите дату ", font=("Arial", 12), justify=tk.LEFT)
        lbl_select_date.pack(side=tk.TOP, pady=5)

        lbl_disc = ttk.Label(
            frame1,
            text="* формат ввода: YYYY-MM-DD",
            font=("Arial", 8),
            justify=tk.LEFT
        )
        lbl_disc.pack(side=tk.TOP, pady=5)

        self.date_entry = ttk.Entry(frame1)
        self.date_entry.pack(side=tk.TOP, pady=10)

        btn_filter = ttk.Button(frame1, text="Фильтр", command=lambda: self.filter_dates(self.date_entry.get()))
        btn_filter.pack(side=tk.TOP, pady=10)

        frame2 = ttk.Frame(records_window, borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        frame2.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.NW)
        lbl_select_exercise = ttk.Label(frame2, text="Введите упражнение ", font=("Arial", 12), justify=tk.LEFT)
        lbl_select_exercise.pack(side=tk.TOP, pady=5)
        self.exercise_entry = ttk.Entry(frame2)
        self.exercise_entry.pack(side=tk.TOP, pady=10)

        btn_filter = ttk.Button(frame2, text="Фильтр", command=lambda: self.filter_exercise(self.exercise_entry.get()))
        btn_filter.pack(side=tk.TOP, pady=10)

        for entry in data:
            tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))

        tree.pack(expand=True, fill=tk.BOTH)

    def filter_dates(self, string_filter: str)->None:
        """Фильтр записей по дате."""
        if string_filter == "":
            pass
        else:
            if self.check_format_date(string_filter):
                self.date_entry.delete(0, tk.END)
                data = self.filtr(volue=string_filter,col="date")
                self.view_records(up=data)
            else:
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(tk.END, "Неверный формат")

    def check_format_date(self, str_:str) -> bool:
        """Проверка формата даты."""
        et = r'[12][09][0-9][0-9]\-[0-1][0-9]\-[0-3][0-9]'
        if re.match(et, str_) :
            return True
        else:
            return False

    def filter_exercise(self, string_filter: str)->None:
        """Фильтр записей по упражнению."""
        if string_filter == "":
            pass
        else:
            self.exercise_entry.delete(0, tk.END)
            data = self.filtr(volue=string_filter, col="exercise")
            self.view_records(up=data)

    def filtr(self, volue:str, col:str)->list:
        """Фильтр записей."""
        data = load_data()
        filtered_data = [d for d in data if volue in d[f'{col}']]
        return filtered_data


def main():
    """Главная функция."""
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
