from PyQt5.QtWidgets import QLabel, QPushButton, QDialog
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import pyqtSignal
import sqlite3

# открывает БД со всеми стилями
con = sqlite3.connect("Design")
cur = con.cursor()


# функция, которая возвращает стиль из БД по имени, выбранным столбцам и таблице
def style(name, select='background-color, border-style, border-width, border-radius, '
                       'border-left-color, border-right-color, border-top-color,'
                       ' border-bottom-color, text-align, font, color', tab='design'):
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


# диалоговое окно для смены дизайна приложения
class Design(QDialog):
    def __init__(self):
        super().__init__()

    # настройка окна
    def initUI(self):
        style_button = style('button')
        style_label = style('label')
        style_end = style('end')
        self.background = style('background', 'background-color').split(': ')[1]

        self.setFixedSize(1020, 650)
        self.setWindowTitle('Выбор дизайна')

        self.label_1 = ClickedLabel(self)
        self.label_1.setGeometry(30, 20, 270, 230)
        self.label_1.setText("")
        self.label_1.setStyleSheet(style_label)
        self.load_image(self.label_1, 'label_1.png')

        self.label_2 = ClickedLabel(self)
        self.label_2.setGeometry(370, 20, 270, 230)
        self.label_2.setText("")
        self.label_2.setStyleSheet(style_label)
        self.load_image(self.label_2, 'label_2.png')

        self.label_3 = ClickedLabel(self)
        self.label_3.setGeometry(710, 20, 270, 230)
        self.label_3.setText("")
        self.label_3.setStyleSheet(style_label)
        self.load_image(self.label_3, 'label_3.png')

        self.label_4 = ClickedLabel(self)
        self.label_4.setGeometry(200, 320, 270, 230)
        self.label_4.setText("")
        self.label_4.setStyleSheet(style_label)
        self.load_image(self.label_4, 'label_4.png')

        self.label_5 = ClickedLabel(self)
        self.label_5.setGeometry(540, 320, 270, 230)
        self.label_5.setText("Пользовательский фон")
        self.label_5.setStyleSheet(style_label)

        self.button = QPushButton(self)
        self.button.setGeometry(750, 580, 200, 40)
        self.button.setStyleSheet(style_button)
        self.button.setText('Выбрать дизайн')

        self.label = QLabel(self)
        self.label.setGeometry(200, 580, 540, 40)
        self.label.setText("")
        self.label.setStyleSheet(style_end)
        self.label.hide()

    # метод добавляет на каждый label изображение дизайна
    def load_image(self, label, name):
        pixmap = QPixmap(name)
        label.setPixmap(pixmap)

    # отображает фоновое изображение или цвет
    def paintEvent(self, event):
        if self.background.endswith('.png'):
            painter = QPainter(self)
            pixmap = QPixmap(self.background)
            painter.drawPixmap(self.rect(), pixmap)
        else:
            self.setStyleSheet(f'background-color: {self.background}')


# пользовательский класс, унаследованный от QLabel, делает их кликабельными
class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ClickedLabel, self).__init__(parent)
        self.click = False

    def mouseReleaseEvent(self, e):  # нажатие на объект
        super().mouseReleaseEvent(e)
        self.clicked.emit()

    def enterEvent(self, e):  # курсор наведен на объект, добавляется рамка
        if not self.click:
            stl = style('label', 'background-color, border-style, border-width, border-radius, text-align, font')
            red = style('end', 'background-color').split(': ')[1]
            borders = f'; border-color: {red}'
            self.setStyleSheet(stl + borders)

    def leaveEvent(self, e):  # курсор покинул объект, убирается рамка
        if not self.click:
            stl = style('label')
            self.setStyleSheet(stl)
