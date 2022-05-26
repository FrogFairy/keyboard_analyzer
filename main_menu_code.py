import sys
import keyboard
from ctypes import *
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import QThread
from main_menu_view import MainWindow, Graph
from design_code import DesignRun
from random import uniform
import csv
import pymorphy2


# класс, унаследованный от класса главного меню с дизайном
class MainWindowRun(MainWindow):
    def __init__(self):  # настройка меню
        super().__init__()
        self.initUI()
        self.design.clicked.connect(self.run_dialog)
        self.start.clicked.connect(self.start_program)
        self.end.clicked.connect(self.end_program)
        self.timer.timeout.connect(self.show_counter)
        self.picture.currentChanged.connect(self.change)
        self.language.activated.connect(self.handleActivated)
        self.save.clicked.connect(self.save_graph)
        self.NewThread = NewThread()

    def save_graph(self):  # метод, сохраняющий статистику программы в виде графика или таблицы
        # статистика запросов, всех слов, русских и английских слов
        global inquiries_data, words_data, rus_data, eng_data
        if self.picture.currentIndex() == 0:
            graph = self.graph_1
            d = inquiries_data
        elif self.picture.currentIndex() == 1:
            graph = self.graph_2
            d = symbols_data
        else:
            graph = self.graph_3
            d = words_data
        if graph is self.graph_3:
            # открытие диалогового окна для выбора пути сохранения
            filename = QFileDialog.getSaveFileName(self, "Сохранить файл", ".",
                                                   "Картинка (*.png);;Таблица всех слов (*.csv);;"
                                                   "Таблица русских слов, которые есть в словаре (*.csv);;"
                                                   "Таблица английских слов, которые есть в словаре (*.csv)")
        else:
            filename = QFileDialog.getSaveFileName(self, "Сохранить файл", ".", "Картинка (*.png);;Таблица (*.csv)")
        if filename[0] and filename[1] == 'Картинка (*.png)':
            graph.figure.savefig(filename[0])
        elif filename[0]:
            # сохранение в виде различных таблиц (формат csv)
            if filename[1] == 'Таблица всех слов (*.csv)':
                data = d
                fieldname = ['слово', 'количество']
            elif filename[1] == 'Таблица русских слов, которые есть в словаре (*.csv)':
                data = rus_words
                fieldname = ['слово', 'количество']
            elif filename[1] == 'Таблица английских слов, которые есть в словаре (*.csv)':
                data = eng_words
                fieldname = ['слово', 'количество']
            else:
                data = d
                fieldname = ['кнопка', 'количество']
            with open(filename[0], 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(fieldname)
                for i in data.items():
                    writer.writerow(i)

    # метод срабатывает при смене языка на вкладке "Частые слова" и перерисовывает график
    def handleActivated(self, index):
        if index == 0:
            self.draw_graph(rus_words, self.graph_3)
        else:
            self.draw_graph(eng_words, self.graph_3)

    # метод срабатывает при смене вкладок на TabWidget
    def change(self):
        try:
            # показывает нужные label и выводит на них информацию
            if self.picture.currentIndex() == 1:
                self.label_3.hide()
                self.language.hide()
                counter = list(map(int, self.label.text()[24:].split(':')))
                counter = counter[0] * 3600 + counter[1] * 60 + counter[2]
                if self.graph_2.picture.text():
                    raise ZeroDivisionError
                global symbols
                self.label_2.setText(f'Средняя скорость набора символов: {(symbols * 60) / counter} символов в минуту')
                self.label_2.show()
            elif self.picture.currentIndex() == 2:
                self.label_2.hide()
                self.language.show()
                self.label_3.show()
            else:
                self.label_3.hide()
                self.language.hide()
                self.label_2.hide()
        except ZeroDivisionError:
            self.label_2.setText('Нет данных для вычисления скорости печати!')
            self.label_2.show()

    # метод начала программы, срабатывает при нажатии на кнопку "Начать"
    def start_program(self):
        # обнуляет всю статистику и таймер, блокирует некоторые кнопки.
        # Также запускает новый поток для считывания действий клавиатуры
        global inquiries_data, symbols_data, words_data, symbols, word
        inquiries_data = {}
        symbols_data = {}
        words_data = {}
        symbols = 0
        word = ''
        self.label.setText('Время работы программы: 00:00:00')
        self.start_timer = True
        self.start.setEnabled(False)
        self.end.setEnabled(True)
        self.picture.setEnabled(False)
        self.save.setEnabled(False)
        self.language.setCurrentIndex(0)
        self.design.setEnabled(False)
        global flag
        flag = True
        self.NewThread.start()

    # метод завершения программы, срабатывает при нажатии на кнопку "Завершить"
    def end_program(self):
        # останавливает таймер, делает активными некоторые кнопки
        global flag
        flag = False
        self.start_timer = False
        self.counter, self.minute, self.second, self.count = 0, '00', '00', '00'
        self.start.setEnabled(True)
        self.end.setEnabled(False)
        self.picture.setEnabled(True)
        self.save.setEnabled(True)
        self.design.setEnabled(True)
        # происходит проверка слов по словарям
        global inquiries_data, words_data, symbols_data, word
        if word in words_data and word:
            words_data[word.lower()] += 1
        elif word not in words_data and word:
            words_data[word.lower()] = 1
        self.search_words(words_data)
        # рисуются графики
        global eng_words, rus_words
        self.draw_graph(inquiries_data, self.graph_1)
        self.draw_graph(symbols_data, self.graph_2)
        self.draw_graph(rus_words, self.graph_3)

    # метод ищет слова в словарях
    def search_words(self, words):
        global eng_words, rus_words
        eng_words = {}
        rus_words = {}
        with open("ENRUS.txt") as word_file:
            en = set(word.strip().lower() for word in word_file)
        with open('zdf-win.txt') as word_file:
            ru = set(word.strip().lower() for word in word_file)
        morph = pymorphy2.MorphAnalyzer()
        for i in words:
            if all(1040 <= ord(j) <= 1103 for j in i):
                p = morph.parse(i)[0]
                if p.normal_form in en or p.normal_form in ru:
                    rus_words[i] = words[i]
            elif i in en and all(65 <= ord(j) <= 90 or 97 <= ord(j) <= 122 for j in i):
                eng_words[i] = words[i]

    # метод рисует график по данным. В случае их отсутствия сообщает об этом пользователю
    def draw_graph(self, data, graph):
        try:
            graph.figure.clear()
            if not data:
                graph.axes = None
                graph.canvas.draw()
                raise IndexError(graph)
            graph.picture.setText('')
            data = list({k: v for k, v in sorted(data.items(), key=lambda x: -int(x[1]))}.items())[:21]
            groups = list(map(lambda x: x[0], data))
            counts = list(map(lambda x: x[1], data))
            colors = [(uniform(self.colors_start, self.colors_end), uniform(self.colors_start, self.colors_end),
                       uniform(self.colors_start, self.colors_end), self.transparency) for _ in range(len(groups))]
            graph.axes = graph.figure.add_subplot()
            graph.axes.bar(groups, counts, width=0.5, color=colors)
            graph.axes.set_xticks(graph.axes.get_xticks())
            graph.axes.set_xticklabels(groups, rotation=50, ha='right')
            graph.axes.grid(axis='y')
            graph.axes.figure.tight_layout()
            graph.axes.patch.set_facecolor(self.label_color)
            graph.axes.patch.set_alpha(1.0)
            graph.canvas.draw()
        except IndexError:
            graph.picture.setText('Нет данных!')

    # показывает таймер
    def show_counter(self):
        if self.start_timer:
            self.counter += 1
            self.count = str(self.counter // 3600).rjust(2, '0')
            self.minute = str((self.counter % 3600) // 60).rjust(2, '0')
            self.second = str((self.counter % 3600) % 60).rjust(2, '0')
            self.label.setText('Время работы программы: {}:{}:{}'.format(self.count, self.minute, self.second))

    # запускает окно смены дизайна при нажатии на соответствующую кнопку
    def run_dialog(self):
        self.des = DesignRun()
        self.des.show()


# пользовательский класс, создает новый поток и считывает действия с клавиатуры пользователя, пока программа работает
class NewThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        global flag, inquiries_data, symbols_data, words_data, symbols, word
        p = {'ctrl': 'left ctrl', 'alt': 'left alt', 'shift': 'left shift'}
        eng = "~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
        rus = "ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
        user32 = windll.user32
        hwnd = user32.GetForegroundWindow()
        threadID = user32.GetWindowThreadProcessId(hwnd, None)
        StartLang = user32.GetKeyboardLayout(threadID)  # определяет раскладку пользователя изначально
        while flag:
            k = keyboard.read_key()
            if keyboard.is_pressed(k):
                # определяет раскладку и сравнивает с начальной, при необходимости меняет букву
                hwnd = user32.GetForegroundWindow()
                threadID = user32.GetWindowThreadProcessId(hwnd, None)
                CodeLang = user32.GetKeyboardLayout(threadID)
                if StartLang != CodeLang and (k in rus or k in eng):
                    k = dict(zip(eng, rus))[k] if k in eng else dict(zip(rus, eng))[k]
                if k in p:
                    k = p[k]
                if k not in inquiries_data:
                    if len(k) == 1:
                        symbols_data[k] = 1
                        symbols += 1
                    inquiries_data[k] = 1
                else:
                    if len(k) == 1:
                        symbols_data[k] += 1
                        symbols += 1
                    inquiries_data[k] += 1
                if k == 'backspace' or k == 'delete':
                    word = word[:-1]
                elif word and len(k) == 1 and (33 <= ord(k) <= 64 or 91 <= ord(k) <= 96 or 123 <= ord(k) <= 126) \
                        or k == 'space' and word or k == 'enter' and word or k == 'backspace' and word:
                    if word.lower() not in words_data:
                        words_data[word.lower()] = 1
                    else:
                        words_data[word.lower()] += 1
                    word = ''
                elif len(k) == 1 and k.isalpha():
                    word += k


# открывает главное окно
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindowRun()
    win.show()
    sys.exit(app.exec_())
