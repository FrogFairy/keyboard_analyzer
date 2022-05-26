from design_view import Design, style
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog
from PIL import Image
import sys
import sqlite3

# открывает БД со всеми стилями
con = sqlite3.connect("Design")
cur = con.cursor()


# функция обновляет данные в БД по имени и параметрам
def update(name, text, tab='design'):
    cur.execute(f"UPDATE {tab} SET {text} WHERE name = '{name}'")
    con.commit()


# класс, унаследованный от класса диалогового окна с дизайном
class DesignRun(Design):
    # настройка окна
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowModality(Qt.ApplicationModal)
        self.choice = False
        self.change_style = False
        self.button.clicked.connect(self.run)
        self.label_1.clicked.connect(self.clicked_label)
        self.label_2.clicked.connect(self.clicked_label)
        self.label_3.clicked.connect(self.clicked_label)
        self.label_4.clicked.connect(self.clicked_label)
        self.label_5.clicked.connect(self.clicked_label)
        self.setMouseTracking(True)

    # нажатие на label. У объекта появляется рамка, но при наведении на другие объекты она не исчезает
    def clicked_label(self):
        self.choice = True
        stl = style('label', 'background-color, border-style, border-width, border-radius, text-align, font')
        red = style('end', 'background-color').split(': ')[1]
        borders = f'; border-color: {red}'
        self.sender().setStyleSheet(stl + borders)
        self.sender().click = True
        self.unclicked_label(self.sender())
        self.choice = self.sender()

    # удаляет рамочку у всех объектов, кроме того, на который нажал пользователь
    def unclicked_label(self, label):
        if label is self.label_1:
            a = [self.label_2, self.label_3, self.label_4, self.label_5]
        elif label is self.label_2:
            a = [self.label_1, self.label_3, self.label_4, self.label_5]
        elif label is self.label_3:
            a = [self.label_1, self.label_2, self.label_4, self.label_5]
        elif label is self.label_4:
            a = [self.label_1, self.label_2, self.label_3, self.label_5]
        else:
            a = [self.label_1, self.label_2, self.label_3, self.label_4]
        stl = style('label')
        for i in a:
            i.setStyleSheet(stl)
            i.click = True

    # основной метод, срабатывает при нажатии на кнопку. В зависимости от нажатого объекта обновляет базу данных
    # и просит пользователя перезапустить приложение, чтобы дизайн обновился
    def run(self):
        try:
            if not self.choice:
                raise IndexError
            if self.choice is self.label_1 or self.choice is self.label_5:
                update('end', 'backgroundColor = "#F4C2C2", borderLeftColor = "#F4C2C2", '
                              'borderRightColor = "#C9A2A2", borderTopColor = "#F4C2C2", '
                              'borderBottomColor = "#C9A2A2", color = "black"')
                update('start', 'backgroundColor = "#96DF96", borderLeftColor = "#96DF96", '
                                'borderRightColor = "#75AF75", borderTopColor = "#96DF96", '
                                'borderBottomColor = "#75AF75", color = "black"')
                update('label', 'backgroundColor = "#C9A0DC", borderLeftColor = "#9878A6", '
                                'borderRightColor = "#9878A6", borderTopColor = "#9878A6", '
                                'borderBottomColor = "#9878A6", color = "black"')
                update('button', 'backgroundColor = "#ADD8E6", borderLeftColor = "#ADD8E6", '
                                 'borderRightColor = "#7C9AA5", borderTopColor = "#ADD8E6", '
                                 'borderBottomColor = " #7C9AA5", color = "black"')
                if self.choice is self.label_1:
                    update('background', 'backgroundColor = "white"')
                else:
                    filename = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '', 'Картинка (*.png)')[0]
                    if filename:
                        im = Image.open(filename)
                        im = im.resize((611, 641))
                        im.save('user.png')
                        update('background', f'backgroundColor = "user.png"')
                update('tab', 'backgroundColor = "#C9A0DC", borderLeftColor = "#9878A6", '
                              'borderRightColor = "#9878A6", borderTopColor = "#9878A6", '
                              'borderBottomColor = "#C9A0DC", color = "black"')
                update('color', 'start = "0", end = "0.996", transparency = "0.6"', 'color')
            elif self.choice is self.label_2:
                update('end', 'backgroundColor = "#560319", borderLeftColor = "#560319", '
                              'borderRightColor = "#2C010D", borderTopColor = "#560319", '
                              'borderBottomColor = "#2C010D", color = "#C1AC04"')
                update('start', 'backgroundColor = "#013220", borderLeftColor = "#013220", '
                                'borderRightColor = "#011C12", borderTopColor = "#013220", '
                                'borderBottomColor = "#011C12", color = "#C1AC04"')
                update('label', 'backgroundColor = "#423189", borderLeftColor = "#2E2262", '
                                'borderRightColor = "#2E2262", borderTopColor = "#2E2262", '
                                'borderBottomColor = "#2E2262", color = "#C1AC04"')
                update('button', 'backgroundColor = "#000080", borderLeftColor = "#000080", '
                                 'borderRightColor = "#00006A", borderTopColor = "#000080", '
                                 'borderBottomColor = " #00006A", color = "#C1AC04"')
                update('background', 'backgroundColor = "black.png"')
                update('tab', 'backgroundColor = "#423189", borderLeftColor = "#2E2262", '
                              'borderRightColor = "#2E2262", borderTopColor = "#2E2262", '
                              'borderBottomColor = "#423189", color = "#C1AC04"')
                update('color', 'start = "0", end = "0.5", transparency = "1"', 'color')
            elif self.choice is self.label_3:
                update('end', 'backgroundColor = "#013220", borderLeftColor = "#013220", '
                              'borderRightColor = "#011C12", borderTopColor = "#013220", '
                              'borderBottomColor = "#011C12", color = "white"')
                update('start', 'backgroundColor = "#D3FEAB", borderLeftColor = "#D3FEAB", '
                                'borderRightColor = "#AFD48D", borderTopColor = "#D3FEAB", '
                                'borderBottomColor = "#AFD48D", color = "black"')
                update('label', 'backgroundColor = "#D9E650", borderLeftColor = "#B1BC3E", '
                                'borderRightColor = "#B1BC3E", borderTopColor = "#B1BC3E", '
                                'borderBottomColor = "#B1BC3E", color = "black"')
                update('button', 'backgroundColor = "#A9EED1", borderLeftColor = "#A9EED1", '
                                 'borderRightColor = "#8AC8AE", borderTopColor = "#A9EED1", '
                                 'borderBottomColor = "#8AC8AE", color = "black"')
                update('background', 'backgroundColor = "#D4FFD5"')
                update('tab', 'backgroundColor = "#D9E650", borderLeftColor = "#B1BC3E", '
                              'borderRightColor = "#B1BC3E", borderTopColor = "#B1BC3E", '
                              'borderBottomColor = "#D9E650", color = "black"')
                update('color', 'start = "0.78", end = "0.996", transparency = "1"', 'color')
            else:
                update('end', 'backgroundColor = "#755330", borderLeftColor = "#755330", '
                              'borderRightColor = "#332515", borderTopColor = "#755330", '
                              'borderBottomColor = "#332515", color = "black"')
                update('start', 'backgroundColor = "#DBA72E", borderLeftColor = "#DBA72E", '
                                'borderRightColor = "#BB8F27", borderTopColor = "#DBA72E", '
                                'borderBottomColor = "#BB8F27", color = "black"')
                update('label', 'backgroundColor = "#F37D53", borderLeftColor = "#D36B46", '
                                'borderRightColor = "#D36B46", borderTopColor = "#D36B46", '
                                'borderBottomColor = "#D36B46", color = "black"')
                update('button', 'backgroundColor = "#E3CCA1", borderLeftColor = "#E3CCA1", '
                                 'borderRightColor = "#BFAC88", borderTopColor = "#E3CCA1", '
                                 'borderBottomColor = "#BFAC88", color = "black"')
                update('background', 'backgroundColor = "autumn.png"')
                update('tab', 'backgroundColor = "#F37D53", borderLeftColor = "#D36B46", '
                              'borderRightColor = "#D36B46", borderTopColor = "#D36B46", '
                              'borderBottomColor = "#F37D53", color = "black"')
                update('color', 'start = "0.5", end = "0.68", transparency = "1"', 'color')
            self.label.setText("Дизайн выбран, для отображения перезапустите приложение!")
            self.label.show()
        except IndexError:
            self.label.setText("Выберите вариант дизайна!")
            self.label.show()
