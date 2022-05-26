import csv
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox
from PyQt5.QtWidgets import QTabWidget, QTabBar, QVBoxLayout
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt
import sqlite3
# открывает БД со всеми стилями
con = sqlite3.connect("Design")
cur = con.cursor()


# функция, которая возвращает стиль из БД по имени, выбранным столбцам и таблице
def style(name, select='background-color, border-style, border-width, border-radius, '
                       'border-left-color, border-right-color, border-top-color, '
                       'border-bottom-color, text-align, font, color', tab='design'):
    field = []
    select = select.split(', ')
    for i in range(len(select)):
        field.append(select[i])
        a = select[i].split('-')
        if len(a) > 2:
            select[i] = ''.join([a[0], a[1][0].upper() + a[1][1:], a[2][0].upper() + a[2][1:]])
        elif len(a) > 1:
            select[i] = ''.join([a[0], a[1][0].upper() + a[1][1:]])
    res = list(cur.execute(f"SELECT {','.join(select)} FROM {tab} WHERE name == '{name}'").fetchall()[0])
    return '; '.join([f'{j}: {i}' for i, j in zip(res, field)])


# класс главного меню
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def initUI(self):  # настройка главного меню
        global style_label, label_color
        style_button = style('button')
        style_label = style('label')
        style_start = style('start')
        style_end = style('end')
        label_color = style('label', 'background-color').split(': ')[1]
        self.label_color = label_color
        self.background = style('background', 'background-color').split(': ')[1]
        a1 = "QTabWidget::pane {%s} " % (style('tab'))
        a2 = "QTabBar::tab:!selected{%s} " % (style('label', 'background-color'))
        a3 = "QTabBar::tab:selected {%s}" % (style('button', 'background-color'))
        self.colors_start = float(style('color', 'start', 'color').split(': ')[1])
        self.colors_end = float(style('color', 'end', 'color').split(': ')[1])
        self.transparency = float(style('color', 'transparency', 'color').split(': ')[1])

        self.setWindowTitle('Главное меню')
        self.setFixedSize(1190, 700)

        self.design = QPushButton(self)
        self.design.setGeometry(10, 30, 200, 40)
        self.design.setStyleSheet(style_button)
        self.design.setText("Изменить дизайн")
        self.design.setFocusPolicy(Qt.NoFocus)

        self.start = QPushButton(self)
        self.start.setGeometry(10, 250, 200, 40)
        self.start.setStyleSheet(style_start)
        self.start.setText("Начать")
        self.start.setFocusPolicy(Qt.NoFocus)

        self.end = QPushButton(self)
        self.end.setGeometry(10, 330, 200, 40)
        self.end.setStyleSheet(style_end)
        self.end.setText("Завершить")
        self.end.setEnabled(False)
        self.end.setFocusPolicy(Qt.NoFocus)

        self.label = QLabel(self)
        self.label.setGeometry(710, 30, 460, 40)
        self.label.setStyleSheet(style_button)
        self.label.setText('Время работы программы: 00:00:00')

        self.label_2 = QLabel(self)
        self.label_2.setGeometry(290, 580, 610, 40)
        self.label_2.setStyleSheet(style_label)
        self.label_2.setText('Средняя скорость набора символов: ')
        self.label_2.hide()

        self.save = QPushButton(self)
        self.save.setGeometry(970, 580, 200, 40)
        self.save.setStyleSheet(style_button)
        self.save.setText("Сохранить")
        self.save.setEnabled(False)
        self.save.setFocusPolicy(Qt.NoFocus)

        self.graph_1 = Graph()
        self.graph_2 = Graph()
        self.graph_3 = Graph()

        self.picture = QTabWidget(self)
        self.picture.setGeometry(290, 100, 880, 450)
        self.picture.addTab(self.graph_1, 'Частые запросы')
        self.picture.addTab(self.graph_2, "Частые символы")
        self.picture.addTab(self.graph_3, "Частые слова")
        self.picture.setStyleSheet(a1 + a2 + a3)
        self.picture.setEnabled(False)

        self.timer = QTimer()
        self.timer.start(1000)
        self.start_timer = False
        self.counter, self.minute, self.second, self.count = 0, '00', '00', '00'

        self.language = QComboBox(self)
        self.language.setGeometry(290, 30, 410, 40)
        self.language.setStyleSheet(style_label + '; selection-color: black')
        self.language.addItem('Русские слова')
        self.language.addItem('Английские слова')
        self.language.setCurrentIndex(0)
        self.language.hide()
        self.language.setFocusPolicy(Qt.NoFocus)

        self.label_3 = QLabel(self)
        self.label_3.setGeometry(290, 580, 610, 40)
        self.label_3.setStyleSheet(style_label)
        self.label_3.setText('На графике изображены только слова, которые присутствуют в словаре!')
        self.label_3.hide()

    def paintEvent(self, event):  # отображает фоновое изображение или цвет
        if self.background.endswith('.png'):
            painter = QPainter(self)
            pixmap = QPixmap(self.background)
            painter.drawPixmap(self.rect(), pixmap)
        else:
            self.setStyleSheet(f'background-color: {self.background}')


# пользовательский класс графиков, унаследованный от QWidget. Создает основу для будущего графика,
# которая потом помещается в TabWidget (self.picture)
class Graph(QWidget):
    def __init__(self):
        super().__init__()
        self.picture = QLabel(self)
        self.picture.setStyleSheet(style_label)
        self.picture.setText("")
        self.figure = Figure()
        self.figure.patch.set_facecolor(label_color)
        self.figure.patch.set_alpha(0.6)
        self.canvas = FigureCanvas(self.figure)
        self.axes = None
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.picture)
        self.setLayout(layout)