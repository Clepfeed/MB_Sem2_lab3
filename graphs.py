import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib.widgets import Button
import re
from collections import defaultdict
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Две функции для сравнения
def reference_function1(x):
    return np.cos(2 * x)

def reference_function2(x):
    return np.sin(np.abs(x)) + 1

# Глобальные переменные
graphs_data = defaultdict(lambda: defaultdict(list))
current_page = 1
unique_numbers = []
show_error_table = False  # Флаг для переключения между графиками и таблицей погрешностей

def calculate_errors(data, function):
    x_points = np.array(data['x_points'])
    y_points = np.array(data['y_points'])
    y_func = function(x_points)
    
    abs_error = np.abs(y_points - y_func)
    rel_error = abs_error / np.abs(y_func) * 100  # в процентах
    
    return {
        'max_abs': np.max(abs_error),
        'avg_abs': np.mean(abs_error),
        'max_rel': np.max(rel_error),
        'avg_rel': np.mean(rel_error)
    }

def toggle_view(event):
    global show_error_table
    show_error_table = not show_error_table
    plot_graphs(current_page)

def switch_page(event):
    global current_page
    current_page = (current_page % len(unique_numbers)) + 1
    plot_graphs(current_page)

def plot_graphs(page_number):
    plt.clf()

    current_number = unique_numbers[page_number - 1]
    current_data = {k: v for k, v in graphs_data[current_number].items() if v}

    if not current_data:
        plt.text(0.5, 0.5, f'Нет данных для номера {current_number}', 
                 horizontalalignment='center', verticalalignment='center')
    else:
        if show_error_table:
            # Создаем заголовки столбцов на основе уникальных первых букв
            columns = []
            for letter in sorted(current_data.keys()):
                columns.append(f"max|{letter}{{1,n}}(x_i) - f_1(x_i)|")
            
            # Создаем данные для таблицы
            cell_text = []
            max_rows = max(len(data_list) for data_list in current_data.values())
            
            # Заполняем таблицу
            for row in range(max_rows):
                row_data = []
                for letter in sorted(current_data.keys()):
                    if row < len(current_data[letter]):
                        data = current_data[letter][row]
                        function = reference_function1 if current_number.endswith('1') else reference_function2
                        errors = calculate_errors(data, function)
                        row_data.append(f"{errors['max_abs']:.6f}")
                    else:
                        row_data.append("")
                cell_text.append(row_data)

            # Создаем таблицу
            ax = plt.gca()
            table = ax.table(cellText=cell_text,
                            colLabels=columns,
                            loc='center',
                            cellLoc='center')
            
            # Настраиваем внешний вид таблицы
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            table.scale(1.2, 1.5)
            
            # Устанавливаем ширину столбцов
            table.auto_set_column_width(col=list(range(len(columns))))
            
            # Убираем оси
            ax.axis('off')
            
            plt.title(f'Таблица погрешностей для номера {current_number}')

        else:
            # Отрисовка графиков
            columns = len(current_data)
            rows = max(len(v) for v in current_data.values())

            for col_idx, (first_letter, data_list) in enumerate(current_data.items()):
                for row_idx, data in enumerate(data_list):
                    ax = plt.subplot(rows, columns, row_idx * columns + col_idx + 1)
                    
                    ax.scatter(data['x_points'], data['y_points'], label='Точки из файла')
                    
                    x = np.linspace(min(data['x_points']), max(data['x_points']), 100)
                    function = reference_function1 if current_number.endswith('1') else reference_function2
                    y = function(x)
                    ax.plot(x, y, 
                            color='blue' if current_number.endswith('1') else 'green', 
                            label=f'Функция {current_number}')
                    
                    ax.set_title(f'График {data["name"]}')
                    ax.grid(True)
                    ax.legend()

            plt.suptitle(f'Графики для номера {current_number}', fontsize=16)

    # Добавляем кнопки
    if hasattr(plot_graphs, 'switch_btn'):
        plot_graphs.switch_btn.ax.set_visible(False)
    if hasattr(plot_graphs, 'toggle_btn'):
        plot_graphs.toggle_btn.ax.set_visible(False)

    switch_btn_ax = plt.axes([0.3, 0.02, 0.2, 0.04])
    toggle_btn_ax = plt.axes([0.55, 0.02, 0.2, 0.04])
    
    plot_graphs.switch_btn = Button(switch_btn_ax, 'Переключить страницу')
    plot_graphs.toggle_btn = Button(toggle_btn_ax, 'Показать/скрыть погрешности')
    
    plot_graphs.switch_btn.on_clicked(switch_page)
    plot_graphs.toggle_btn.on_clicked(toggle_view)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)
    plt.draw()

# Остальной код остается без изменений
directory = "./"
script_dir = os.path.dirname(os.path.abspath(__file__))
dir_path = os.path.join(script_dir, directory)
files = [f for f in os.listdir(dir_path) if f.endswith('.txt')]

for file_name in files:
    x_points = []
    y_points = []
    
    with open(os.path.join(dir_path, file_name), 'r') as file:
        for line in file:
            values = line.strip().split()
            if len(values) == 2:
                try:
                    x = float(values[0])
                    y = float(values[1])
                    x_points.append(x)
                    y_points.append(y)
                except ValueError:
                    print(f"Пропущена строка в файле {file_name}: {line}")
    
    match = re.search(r'_(\d+)', file_name)
    if match:
        number = match.group(1)
        first_letter = file_name[0]
        
        data = {
            'name': file_name,
            'x_points': x_points,
            'y_points': y_points
        }
        
        graphs_data[number][first_letter].append(data)
        
        if number not in unique_numbers:
            unique_numbers.append(number)

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

window_width = int(screen_width * 0.85)
window_height = int(screen_height * 0.85)
position_x = int((screen_width - window_width) / 2)
position_y = int((screen_height - window_height) / 2)

root = tk.Tk()
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

fig = plt.figure(figsize=(window_width / 100, window_height / 100))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

plot_graphs(1)

root.mainloop()