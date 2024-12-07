"""
Журнал тренировок
"""
import csv
import json
import datetime

import tkinter as tk
from tkinter import ttk, Toplevel, messagebox, simpledialog
from tkinter.constants import RIGHT
import matplotlib.pyplot as plt

from tkcalendar import DateEntry

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

class DataTimePicker(tk.Frame):
    def __init__(self, parent, *args, **kwrgs):
        super().__init__(parent, *args, **kwrgs)

        self.date_entry = DateEntry(self, width=10, background='darkblue', foreground='white', borderwidth=2,)
        self.date_entry.pack(side=tk.LEFT, padx=(0,5))

        self.hour_spin = ttk.Spinbox(self, from_=0, to=23, width=3, increment=1, format='%02.0f')
        self.hour_spin.pack(side=tk.LEFT)

        self.minute_spin = ttk.Spinbox(self, from_=0, to=59, width=3, format='%02.0f')
        self.minute_spin.pack(side=tk.LEFT)

    def get(self):
        date_str = self.date_entry.get()
        time_str = f"{self.hour_spin.get()}:{self.minute_spin.get()}"
        return f"{date_str} {time_str}"


class TrainingLogApp:
    """
    Класс для ведения дневника тренировок.
    """
    def __init__(self, root):
        self.root = root
        root.title("Дневник тренировок")
        self.create_widgets()

    def create_widgets(self):
        """Создание виджетов."""
        # Виджеты для ввода данных
        self.datetime_picker = DataTimePicker(self.root)
        self.datetime_picker.grid(column=0, row=0, columnspan=2, sticky=tk.EW)

        self.exercise_label = ttk.Label(self.root, text="Упражнение:")
        self.exercise_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.exercise_entry = ttk.Entry(self.root)
        self.exercise_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        self.weight_label = ttk.Label(self.root, text="Вес:")
        self.weight_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        self.repetitions_label = ttk.Label(self.root, text="Повторения:")
        self.repetitions_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

        self.repetitions_entry = ttk.Entry(self.root)
        self.repetitions_entry.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)

        self.add_button = ttk.Button(self.root, text="Добавить запись", command=self.add_entry)
        self.add_button.grid(column=0, row=4, columnspan=2, pady=10)

        self.view_button = ttk.Button(self.root, text="Просмотреть записи", command=self.view_records)
        self.view_button.grid(column=0, row=5, columnspan=2, pady=10)

    def add_entry(self):
        """Добавление записи."""
        date = self.datetime_picker.get()
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
        self.records_window = Toplevel(self.root)
        self.records_window.title("Записи тренировок")
        place_ = ttk.Frame(self.records_window, padding=10,relief=tk.RIDGE)
        place_.pack()
        self.tree = ttk.Treeview(place_, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        self.tree.heading('Дата', text="Дата")
        self.tree.heading('Упражнение', text="Упражнение")
        self.tree.heading('Вес', text="Вес")
        self.tree.heading('Повторения', text="Повторения")
        self.scrollbar = ttk.Scrollbar(place_, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)#
        btn = ttk.Button(self.records_window, text="Закрыть", command=self.records_window.destroy)
        btn.pack(side=tk.BOTTOM, pady=10)

        frame1 = ttk.Frame(self.records_window, borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        frame1.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.NW)

        lbl_select_date = ttk.Label(frame1, text="Введите интервал даты", font=("Arial", 12), justify=tk.LEFT)
        lbl_select_date.pack(side=tk.TOP, pady=5)

        lbl_disc = ttk.Label(
            frame1,
            text="С:",
            font=("Arial", 8),
            justify=tk.LEFT
        )
        lbl_disc.pack(side=tk.TOP, pady=5)
        datetime_picker1 = DataTimePicker(frame1)
        datetime_picker1.pack(side=tk.TOP, pady=10)
        lbl_disc2 = ttk.Label(
            frame1,
            text="ПО:",
            font=("Arial", 8),
            justify=tk.LEFT
        )
        lbl_disc2.pack(side=tk.TOP, pady=5)
        datetime_picker2 = DataTimePicker(frame1)
        datetime_picker2.pack(side=tk.TOP, pady=10)

        btn_filter = ttk.Button(frame1, text="Фильтр", command=lambda: self.filter_dates(datetime_picker1.get(),
                                                                                         datetime_picker2.get()))
        btn_filter.pack(side=tk.TOP, pady=10)

        frame2 = ttk.Frame(self.records_window, borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        frame2.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.NW)
        lbl_select_exercise = ttk.Label(frame2, text="Введите упражнение ", font=("Arial", 12), justify=tk.LEFT)
        lbl_select_exercise.pack(side=tk.TOP, pady=5)
        self.exercise_entry = ttk.Entry(frame2)
        self.exercise_entry.pack(side=tk.TOP, pady=10)

        btn_filter = ttk.Button(frame2, text="Фильтр", command=lambda: self.filter_exercise(self.exercise_entry.get()))
        btn_filter.pack(side=tk.TOP, pady=10)

        frame3 = ttk.Frame(self.records_window, borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        frame3.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.NW)
        btn_export = ttk.Button(frame3, text="Экспорт в CSV", command=lambda: self.export_records())
        btn_export.pack(side=tk.TOP, pady=10)
        btn_import = ttk.Button(frame3, text="Импорт из CSV", command=lambda: self.import_records())
        btn_import.pack(side=tk.TOP, pady=10)

        frame4 = ttk.Frame(self.records_window, borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        frame4.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.NW)
        btn_edit = ttk.Button(frame4, text="Редактировать запись", command=lambda: self.edit_records(self.tree.selection()))
        btn_edit.pack(side=tk.TOP, pady=10)
        btn_delete = ttk.Button(frame4, text="Удалить запись", command=lambda: self.delete_records(self.tree.index(self.tree.selection())))
        btn_delete.pack(side=tk.TOP, pady=10)

        frame5 = ttk.Frame(self.records_window, borderwidth=1, relief=tk.SOLID, padding=[8, 1])
        frame5.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.NW)
        lbl_statistics1 = ttk.Label(frame5, text="Статистика", font=("Arial", 12), justify=tk.LEFT)
        lbl_statistics1.pack(side=tk.TOP, pady=5)
        lbl_statistics2 = ttk.Label(frame5, text="Суммарный вес:", font=("Arial", 10), justify=tk.LEFT)
        lbl_statistics2.pack(side=tk.TOP, pady=5)

        for entry in data:
            self.tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))

        sum_weight = self.total_weight(data)
        lbl_statistics3 = ttk.Label(frame5, text=sum_weight, font=("Arial", 10), justify=tk.LEFT)
        lbl_statistics3.pack(side=tk.TOP, pady=5)
        self.tree.pack(expand=True, fill=tk.BOTH)
        btn_grafic = ttk.Button(frame5, text="Показать\nграфик", command=lambda: self.view_grafic())
        btn_grafic.pack(side=tk.TOP, pady=5)

    def date_to_unix(self, date: str)->int:
        d = date[:10]
        date = datetime.datetime.strptime(d, "%d.%m.%Y")
        unix = date.timestamp()
        return unix

    def filter_dates(self, date1_filter: str, date2_filter: str)->None:
        date1 = self.date_to_unix(date1_filter)
        date2 = self.date_to_unix(date2_filter)
        data = load_data()
        filtered_data = [d for d in data if date1 <= self.date_to_unix(d['date']) <= date2]
        self.records_window.destroy()
        self.view_records(up=filtered_data)

    def filter_exercise(self, string_filter: str)->None:
        """Фильтр записей по упражнению."""
        if string_filter == "":
            pass
        else:
            self.exercise_entry.delete(0, tk.END)
            data = self.filtr(volue=string_filter, col="exercise")
            self.records_window.destroy()
            self.view_records(up=data)

    def filtr(self, volue:str, col:str)->list:
        """Фильтр записей."""
        data = load_data()
        filtered_data = [d for d in data if volue in d[f'{col}']]
        return filtered_data

    def total_weight(self, data:list)->float:
        total = 0
        for entry in data:
            total += float(entry["weight"])
        return total

    def export_records(self)->None:
        """Экспорт записей в CSV."""
        data = load_data()
        with open("training_log.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(("Дата", "Упражнение", "Вес", "Повторения"))
            for entry in data:
                writer.writerow((entry["date"], entry["exercise"], entry["weight"], entry["repetitions"]))
            messagebox.showinfo("Успешно", "Записи успешно экспортированы!")

    def import_records(self)->None:
        """Импорт записей из CSV."""
        try:
            with open("training_log.csv", "r") as f:
                reader = csv.reader(f)
                data = list(reader)
                list_ = []
                keys = ["date", "exercise", "weight", "repetitions"]
                len_ = len(data)
                for item in data[1:len_]:
                    list_.append(dict(zip(keys, item)))
                save_data(list_)
                messagebox.showinfo("Успешно", "Записи успешно импортированы!")
                self.records_window.destroy()
                self.view_records(up=list_)
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл не найден!")

    def edit_records(self, selected_item)->None:
        """Редактирование записей."""
        if not selected_item:
            return
        item_values = self.tree.item(selected_item, "values")

        new_date = simpledialog.askstring("Редактирование даты", "Введите дату:", initialvalue=item_values[0])
        new_exersice = simpledialog.askstring("Редактирование упражнения", "Введите новое упражнение:",
                                         initialvalue=item_values[1])
        new_weight = simpledialog.askfloat("Редактирование веса", "Введите новый вес:", initialvalue=item_values[2])
        new_repetitions = simpledialog.askinteger("Редактирование повторений", "Введите новое количество повторений:",
                                       initialvalue=item_values[3])

        if new_date and new_exersice and new_weight and new_repetitions:
            # Обновляем запись
            self.tree.item(selected_item, values=(new_date, new_exersice, new_weight, new_repetitions))
        data = []
        for item in self.tree.get_children():
            item_data = self.tree.item(item)
            data.append(item_data['values'])  # Сохраняем значения
        list_ = []
        keys = ["date", "exercise", "weight", "repetitions"]
        # len_ = len(data)
        for item in data:
            list_.append(dict(zip(keys, item)))
        save_data(list_)
        self.records_window.destroy()
        self.view_records(up=list_)

    def delete_records(self, selected_item:int)->None:
        """Удаление записей"""
        if not selected_item:
            return
        data = load_data()
        del data[selected_item]
        save_data(data)
        self.records_window.destroy()
        self.view_records(up=data)

    def view_grafic(self):
        data1 = []
        data2 = []
        selected_item = self.tree.get_children()
        lab = [l for l in range(1, len(self.tree.get_children()) + 1)]
        for item in selected_item:
            item_data = self.tree.item(item)
            data1.append(float(item_data['values'][2]))
            data2.append(item_data['values'][3])

        # Создание графика
        plt.figure(figsize=(10, 5))  # Размер графика
        plt.plot(lab, data1, '-o', label='Вес')  # ��иния с маркерами для каждого значения)  # Линия с маркерами для каждого значения
        plt.plot(lab, data2, '-*', label='Количество повторений')  # ��иния с маркерами для каждого значения


        # Настройка графика
        plt.title('График количества повторений и весов')  # Заголовок графика
        plt.xlabel('Метки')  # Подпись для оси X
        plt.ylabel('Значения')  # Подпись для оси Y
        plt.legend(loc='best')  # Подпись меток
        plt.grid()  # Включение сетки

        # Показать график
        plt.savefig('plot.png')  # Сохранить график как файл
        plt.show()  # Отображение графика



def main():
    """Главная функция."""
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
