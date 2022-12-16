import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QListWidgetItem, QInputDialog


class LinExp(Exception):
    pass


class NumExp(Exception):
    pass


class OstExp(Exception):
    pass


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('proekt_izm.ui', self)
        self.setFixedSize(1000, 1000)
        self.setWindowTitle('Изменение викторины')
        self.con = sqlite3.connect('viktorina.db')
        self.cur = self.con.cursor()

        # инициируем box
        c = self.cur.execute("""SELECT id FROM voprosi""").fetchall()
        self.con.commit()
        fl = 0
        for i in c:
            self.comboBox.addItem(str(i[0]))
            self.comboBox_3.addItem(str(i[0]))
            self.comboBox_4.addItem(str(i[0]))
            self.comboBox_6.addItem(str(i[0]))
            self.comboBox_7.addItem(str(i[0]))
            fl = 1

        # Инициируем боксы с вопросами
        if len(c) > 0 and fl == 1:
            ot = self.cur.execute(f"""SELECT id FROM otveti WHERE vopros={c[0][0]}""").fetchall()
            for i in ot:
                self.comboBox_5.addItem(str(i[0]))
                self.comboBox_8.addItem(str(i[0]))
            # И ответы
            if len(ot) > 0:
                ov = self.cur.execute(
                    f"""SELECT text FROM otveti WHERE id = {self.comboBox_6.currentText()}""").fetchone()
                if ov:
                    self.lineEdit_6.setText(ov[0])
                ov1 = self.cur.execute(f"""SELECT text, pravilno FROM 
                otveti WHERE id = {self.comboBox_8.currentText()}""").fetchone()
                if ov1:
                    self.lineEdit_8.setText(ov1[0])
                    self.lineEdit_6.setText(ov1[0])
                    if ov1[1]:
                        self.checkBox_2.setCheckState(True)
                    else:
                        self.checkBox_2.setCheckState(False)

        # даем значения линиям, если есть вопросы
        if fl == 1:
            red = self.cur.execute(f"""SELECT * FROM voprosi WHERE id = {c[0][0]}""").fetchone()
            self.con.commit()
            self.lineEdit_4.setText(red[1])
            self.lineEdit_5.setText(red[1])
            self.lineEdit_9.setText(red[1])
            self.lineEdit_10.setText(red[1])
            self.lineEdit_7.setText(red[1])

        # находим стартовый id для вопросов
        a = (self.cur.execute("""SELECT COUNT(*) FROM voprosi""").fetchone())[0]
        if a == 0:
            self.count = 1
        else:
            self.count = self.cur.execute("""SELECT MAX(id) FROM voprosi""").fetchone()[0] + 1

        # и для ответов
        a1 = (self.cur.execute("""SELECT COUNT(*) FROM otveti""").fetchone())[0]
        if a1 == 0:
            self.otv_count = 1
        else:
            self.otv_count = self.cur.execute("""SELECT MAX(id) FROM otveti""").fetchone()[0] + 1
        self.con.commit()
        self.initUI()

    def initUI(self):
        # подключаем все кнопки
        self.pushButton.clicked.connect(self.show_window_2)
        self.but1.clicked.connect(self.run)
        self.but1_12.clicked.connect(self.run1)
        self.but1_2.clicked.connect(self.dob_vopr)
        self.but1_3.clicked.connect(self.dobavit_otvet)
        self.but1_4.clicked.connect(self.udal_vopr)
        self.but1_5.clicked.connect(self.udal_posl_vopr)
        self.but1_6.clicked.connect(self.udal_posl_otvet)
        self.but1_7.clicked.connect(self.udal_otv)
        self.but1_8.clicked.connect(self.izmenit_vopr)
        self.but1_9.clicked.connect(self.izmenit_otvet)
        self.but1_10.clicked.connect(self.show_window_1)
        self.but1_11.clicked.connect(self.show_window_3)
        self.comboBox.activated.connect(self.izm_zn_1)
        self.comboBox_3.activated.connect(self.izm_zn_2)
        self.comboBox_4.activated.connect(self.izm_zn_3)
        self.comboBox_6.activated.connect(self.izm_zn_4)
        self.comboBox_7.activated.connect(self.izm_zn_5)
        self.comboBox_5.activated.connect(self.izm_zn_6)
        self.comboBox_8.activated.connect(self.izm_zn_7)

    def run(self):
        self.int_num, ok_pressed = QInputDialog.getItem(
            self, "Вы уверены?", "Вы уверены?", ("Да", "Нет"), 1, False)
        if ok_pressed and self.int_num == "Да":
            self.dele_tab()

    def run1(self):
        self.int_num, ok_pressed = QInputDialog.getItem(
            self, "Вы уверены?", "Вы уверены?", ("Да", "Нет"), 1, False)
        if ok_pressed and self.int_num == "Да":
            self.del_rat()

        # Здесь диалоговые окна

    def dele_tab(self):
        # Удаляем все из таблицы
        self.cur.execute("""DELETE from voprosi""")
        self.cur.execute("""DELETE from otveti""")
        self.con.commit()
        self.ochistit()

    def del_rat(self):
        # удаляем рейтинг
        self.cur.execute("""DELETE from rating""")
        self.con.commit()

    def dob_vopr(self):
        # Доьавляем
        self.label_5.setText("")
        try:
            if self.lineEdit_2.text() == "":
                raise LinExp
            if len(self.lineEdit_2.text()) >= 1000:
                raise NumExp
            st = """INSERT INTO voprosi
                                   (id, text)
                                   VALUES (?, ?);"""
            data_tuple = (self.count, self.lineEdit_2.text())
            self.cur.execute(st, data_tuple)
            self.con.commit()
            c = self.cur.execute("""SELECT * FROM voprosi""").fetchall()
            self.con.commit()

            # обновляем combobox
            self.obnova_box()
            if len(c) >= 1:
                red = self.cur.execute(f"""SELECT * FROM voprosi WHERE id = {c[0][0]}""").fetchone()
                self.con.commit()
                self.lineEdit_4.setText(red[1])
                self.lineEdit_5.setText(red[1])
                self.lineEdit_9.setText(red[1])
                self.lineEdit_10.setText(red[1])
                self.lineEdit_7.setText(red[1])
            self.label_5.setText("ok")

            # Добавляем, чтобы получить новый id
            self.count += 1
        except LinExp:
            self.label_5.setText("Вопрос не должен состоять из пустоты")
        except NumExp:
            self.label_5.setText("Вопрос должнен быть меньше 1000 символов!")

    def udal_posl_vopr(self):
        self.label_5.setText("ok")
        a = (self.cur.execute("""SELECT COUNT(*) FROM voprosi""").fetchone())[0]
        # А вдруг ничего нет?
        try:
            if a == 0:
                raise NumExp
            self.label_5.setText("ok")
            idi = self.cur.execute("SELECT * FROM voprosi ORDER BY id DESC LIMIT 1").fetchone()
            self.cur.execute(f"DELETE FROM voprosi WHERE id={idi[0]}")
            self.cur.execute(f"DELETE FROM otveti WHERE vopros={idi[0]}")
            self.con.commit()
            self.comboBox_5.clear()
            self.comboBox_8.clear()
            self.obnova_box()
            #  Если ничего не стало - не ставим новых значений в линии, так как
            if a != 1:
                self.izm_zn_1()
                self.izm_zn_2()
                self.izm_zn_3()
                self.izm_zn_4()
                self.izm_zn_5()
            if a == 1:
                self.ochistit()
            self.con.commit()
        except NumExp:
            self.label_5.setText("Удаление невозможно: Вопросов больше нет!")

    def izm_zn_1(self):
        # Обновляем лайны
        red = self.cur.execute(f"""SELECT * FROM voprosi WHERE id = {self.comboBox.currentText()}""").fetchone()
        self.lineEdit_4.setText(red[1])
        self.con.commit()

    def izm_zn_2(self):
        red = self.cur.execute(f"""SELECT * FROM voprosi WHERE id = {self.comboBox_3.currentText()}""").fetchone()
        self.lineEdit_5.setText(red[1])
        self.con.commit()

    def izm_zn_3(self):
        red = self.cur.execute(f"""SELECT * FROM voprosi WHERE id = {self.comboBox_4.currentText()}""").fetchone()
        self.con.commit()
        self.comboBox_5.clear()
        if len(red) > 0:
            # в 3 и 5 мы также должны обновить боксы с ответами для каждого вопроса
            ot = self.cur.execute(f"""SELECT id FROM otveti WHERE vopros={self.comboBox_4.currentText()}""").fetchall()
            for i in ot:
                self.comboBox_5.addItem(str(i[0]))
            if self.comboBox_5.currentText():
                ov = self.cur.execute(f"""SELECT text FROM otveti WHERE id = 
                                       {self.comboBox_5.currentText()}""").fetchone()
                self.lineEdit_6.setText(ov[0])
            else:
                self.lineEdit_6.setText("")

        self.lineEdit_9.setText(red[1])
        self.con.commit()

    def izm_zn_4(self):
        red = self.cur.execute(f"""SELECT * FROM voprosi WHERE id = {self.comboBox_6.currentText()}""").fetchone()
        self.lineEdit_7.setText(red[1])
        self.con.commit()

    def izm_zn_5(self):
        red = self.cur.execute(f"""SELECT * FROM voprosi WHERE id = {self.comboBox_7.currentText()}""").fetchone()
        self.lineEdit_10.setText(red[1])
        self.con.commit()
        self.comboBox_8.clear()
        if len(red) > 0:
            ot = self.cur.execute(f"""SELECT id FROM otveti WHERE vopros={self.comboBox_7.currentText()}""").fetchall()
            for i in ot:
                self.comboBox_8.addItem(str(i[0]))
            if self.comboBox_8.currentText():
                if self.comboBox_8.currentText():
                    ov = self.cur.execute(f"""SELECT text, pravilno FROM otveti 
                    WHERE id = {self.comboBox_8.currentText()}""").fetchone()
                    self.lineEdit_8.setText(ov[0])
                    #  в пятом также нужно вывести правильность ответа
                    if ov and ov[1]:
                        self.checkBox_2.setCheckState(True)
                    else:
                        self.checkBox_2.setCheckState(False)
            else:
                self.lineEdit_8.setText("")
                self.checkBox_2.setCheckState(False)

        self.con.commit()

    def izm_zn_6(self):
        # В 6 и 7 обновляем линии для ответов
        con = sqlite3.connect('viktorina.db')
        cur = con.cursor()
        red = cur.execute(f"""SELECT * FROM voprosi WHERE id = {self.comboBox_4.currentText()}""").fetchone()
        con.commit()
        if len(red) > 0:
            if self.comboBox_5.currentText() != "":
                ove = cur.execute(f"""SELECT text FROM otveti WHERE id = {self.comboBox_5.currentText()}""").fetchone()
                self.lineEdit_6.setText(ove[0])
        else:
            self.lineEdit_6.setText("")
            self.checkBox_2.setCheckState(False)

    def izm_zn_7(self):
        red = self.cur.execute(f"""SELECT * FROM voprosi WHERE id = {self.comboBox_7.currentText()}""").fetchone()
        self.con.commit()
        if len(red) > 0:
            ov = self.cur.execute(f"""SELECT text, pravilno FROM 
            otveti WHERE id = {self.comboBox_8.currentText()}""").fetchone()
            self.con.commit()
            self.lineEdit_8.setText(ov[0])
            if ov[1]:
                self.checkBox_2.setCheckState(True)
            else:
                self.checkBox_2.setCheckState(False)
        else:
            self.lineEdit_8.setText("")
            self.checkBox_2.setCheckState(False)

    def dobavit_otvet(self):
        con = sqlite3.connect('viktorina.db')
        cur = con.cursor()
        self.label_9.setText("")
        st = """INSERT INTO otveti
                               (id, vopros, text, pravilno)
                               VALUES (?, ?, ?, ?);"""
        try:
            if self.comboBox.currentText() == "":
                raise OstExp

            if self.lineEdit_3.text() == "":
                raise LinExp
            if len(self.lineEdit_3.text()) >= 1000:
                raise NumExp
            data_tuple = (
                self.otv_count, int(self.comboBox.currentText()), self.lineEdit_3.text(), self.checkBox.isChecked())
            self.otv_count += 1
            cur.execute(st, data_tuple)
            con.commit()
            self.label_9.setText("ok")
            self.izm_zn_5()
            self.izm_zn_3()
        except LinExp:
            self.label_9.setText("Ответ не может быть пустым!")
        except NumExp:
            self.label_9.setText("Длина должна быть меньше 1000 символов!")
        except OstExp:
            self.label_9.setText("Вы не добавили ни одного вопроса!")
        con.commit()
        con.close()

    def udal_posl_otvet(self):
        self.label_9.setText("")
        a = (self.cur.execute("""SELECT COUNT(*) FROM otveti""").fetchone())[0]
        if a != 0:
            self.label_9.setText("ok")
            idi = self.cur.execute("SELECT * FROM otveti ORDER BY id DESC LIMIT 1").fetchone()
            self.cur.execute(f"DELETE FROM otveti WHERE id={idi[0]}")
            self.label_9.setText("ok")
            self.con.commit()
            self.izm_zn_5()
            self.izm_zn_3()
        else:
            self.label_9.setText("Удаление невозможно: ответов больше нет!")
        if a == 1:
            self.otv_count = 1

    def udal_vopr(self):
        self.label_10.setText("")
        a = (self.cur.execute("""SELECT COUNT(*) FROM voprosi""").fetchone())[0]
        if a != 0:
            idi = self.comboBox_3.currentText()
            self.cur.execute(f"DELETE FROM voprosi WHERE id={idi}")
            self.cur.execute(f"DELETE FROM otveti WHERE vopros={idi}")
            self.con.commit()

            self.comboBox_5.clear()
            self.comboBox_8.clear()
            self.obnova_box()

            if a != 1:
                self.izm_zn_1()
                self.izm_zn_2()
                self.izm_zn_3()
                self.izm_zn_4()
                self.izm_zn_5()
            self.label_10.setText("ok")
        else:
            self.label_10.setText("Удаление невозможно: Вопросов больше нет!")
        if a == 1:
            self.count = 1
            self.otv_count = 1

            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")
            self.lineEdit_6.setText("")
            self.lineEdit_7.setText("")
            self.lineEdit_8.setText("")
            self.checkBox_2.setCheckState(False)
            self.lineEdit_9.setText("")
            self.lineEdit_10.setText("")

    def izmenit_vopr(self):
        self.label_15.setText("")
        a = (self.cur.execute("""SELECT COUNT(*) FROM voprosi""").fetchone())[0]
        if self.lineEdit_7.text() != "" and len(self.lineEdit_7.text()) < 1000 and a != 0:
            # просто обновляем
            idi = int(self.comboBox_6.currentText())
            self.cur.execute(f"""UPDATE voprosi SET text = '{self.lineEdit_7.text()}' WHERE id = {idi}""")
            self.con.commit()

            # Обновляем боксы и линии
            self.obnova_box()

            self.izm_zn_1()
            self.izm_zn_2()
            self.izm_zn_3()
            self.izm_zn_4()
            self.izm_zn_5()
            self.label_15.setText("ok")
        elif self.lineEdit_7.text() == "":
            self.label_15.setText("Вопрос не должен быть пустым!")
        elif a == 0:
            self.label_15.setText("Вопроса не существует")
        else:
            self.label_15.setText("Вопрос должен быть меньше 1000 символов!")

    def obnova_box(self):
        # Здесь просто частоповторяющаяся функция
        c = self.cur.execute("""SELECT * FROM voprosi""").fetchall()
        self.comboBox.clear()
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        self.comboBox_6.clear()
        self.comboBox_7.clear()
        for i in c:
            self.comboBox.addItem(str(i[0]))
            self.comboBox_3.addItem(str(i[0]))
            self.comboBox_4.addItem(str(i[0]))
            self.comboBox_6.addItem(str(i[0]))
            self.comboBox_7.addItem(str(i[0]))
        self.con.commit()

    def udal_otv(self):
        self.label_13.setText("")
        a = (self.cur.execute(f"""SELECT COUNT(*) FROM otveti WHERE 
                              vopros={self.comboBox_4.currentText()}""").fetchone())[0]
        al = (self.cur.execute(f"""SELECT COUNT(*) FROM otveti""").fetchone())[0]
        if a != 0 and al != 0 and self.comboBox_5.currentText() != "":  # Смотрим остались ли вообще ответы
            idi = self.comboBox_5.currentText()
            self.cur.execute(f"DELETE FROM otveti WHERE id={idi}")
            self.con.commit()

            self.comboBox_5.clear()
            self.comboBox_8.clear()
            self.izm_zn_5()
            self.izm_zn_3()
            self.obnova_box()
            if a != 1:
                self.izm_zn_6()
                self.izm_zn_7()
            self.label_13.setText("ok")
        else:
            self.label_13.setText("Удаление невозможно: ответов больше нет или он не выбран!")
        if al == 1:
            self.otv_count = 1
            self.lineEdit_6.setText("")
            self.lineEdit_8.setText("")
            self.checkBox_2.setCheckState(False)

    def izmenit_otvet(self):
        self.label_15.setText("")
        a = (self.cur.execute(f"""SELECT COUNT(*) FROM otveti WHERE vopros=
                              {self.comboBox_7.currentText()}""").fetchone())[0]
        if self.lineEdit_8.text() != "" and len(self.lineEdit_8.text()) < 1000 and a != 0 and \
                self.comboBox_8.currentText() != "":
            idi = int(self.comboBox_8.currentText())
            self.cur.execute(f"""UPDATE otveti SET text = '{self.lineEdit_8.text()}' WHERE id = {idi}""")
            self.cur.execute(f"""UPDATE otveti SET pravilno = {self.checkBox_2.isChecked()} WHERE id = {idi}""")
            self.con.commit()

            self.obnova_box()
            self.izm_zn_1()
            self.izm_zn_2()
            self.izm_zn_3()
            self.izm_zn_4()
            self.izm_zn_5()
            self.label_15.setText("ok")
        elif self.lineEdit_8.text() == "":
            self.label_17.setText("Ответ не должен быть пустым!")
        elif a == 0 or self.comboBox_8.currentText() == "":
            self.label_17.setText("Ответа не существует")
        else:
            self.label_17.setText("Ответ должен быть меньше 1000 символов!")

    def ochistit(self):
        # Очищение дизайна
        self.count = 1
        self.otv_count = 1
        self.comboBox.clear()
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        self.comboBox_5.clear()
        self.comboBox_6.clear()
        self.comboBox_7.clear()
        self.comboBox_8.clear()
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_8.setText("")
        self.checkBox_2.setCheckState(False)
        self.lineEdit_9.setText("")
        self.lineEdit_10.setText("")
        self.label_5.setText("")
        self.label_9.setText("")
        self.label_10.setText("")
        self.label_13.setText("")
        self.label_15.setText("")
        self.label_17.setText("")

    # Далее - переходы на другие окна
    def show_window_2(self):
        self.w2 = Window2()
        self.w2.show()
        self.close()

    def show_window_1(self):
        self.w1 = Window1()
        self.w1.show()
        self.close()

    def show_window_3(self):
        self.w3 = Window3()
        self.w3.show()
        self.close()


class Window2(QMainWindow):
    def __init__(self):
        super(Window2, self).__init__()
        self.w3 = Window3()
        self.w1 = Window1()
        self.w2 = MyWidget()
        uic.loadUi('lideri.ui', self)
        self.setWindowTitle('Таблица прохождений')
        self.pushButton.clicked.connect(self.show_window_2)
        self.pushButton_2.clicked.connect(self.show_window_1)
        self.pushButton_3.clicked.connect(self.show_window_3)
        self.con = sqlite3.connect("viktorina.db")
        self.cur = self.con.cursor()
        self.search()

    def search(self):
        # Отображаем таблицу с участниками
        res = self.cur.execute(f'SELECT balli, name, percents, maximum FROM rating').fetchall()
        if res:
            self.tableWidget.setRowCount(len(res))
            self.tableWidget.setColumnCount(len(res[0]))
        for i, elem in enumerate(res):
            if i == 0:
                self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Набрано баллов"))
                self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Имя участника"))
                self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Проценты"))
                self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Макс. баллов"))
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def show_window_2(self):
        self.w2.show()
        self.close()

    def show_window_1(self):
        self.w1.show()
        self.close()

    def show_window_3(self):
        self.w3.show()
        self.close()


class Window1(QMainWindow):
    def __init__(self):
        super(Window1, self).__init__()
        uic.loadUi('prosmotr.ui', self)
        self.setFixedSize(1000, 1000)
        self.setWindowTitle('Просмотор викторины')
        self.pushButton.clicked.connect(self.show_window_2)
        self.pushButton_2.clicked.connect(self.show_window_1)
        self.pushButton_3.clicked.connect(self.show_window_3)
        self.con = sqlite3.connect("viktorina.db")
        self.cur = self.con.cursor()
        self.search()

    def show_window_2(self):
        self.w2 = MyWidget()
        self.w2.show()
        self.close()

    def show_window_1(self):
        self.w1 = Window2()
        self.w1.show()
        self.close()

    def show_window_3(self):
        self.w3 = Window3()
        self.w3.show()
        self.close()

    def search(self):
        res = self.cur.execute(f'SELECT id, text FROM voprosi').fetchall()
        self.con.commit()
        for i, elem in enumerate(res):
            res1 = self.cur.execute(f'SELECT pravilno, text FROM otveti WHERE vopros = {elem[0]}').fetchall()
            self.con.commit()
            for j, val in enumerate(res1):
                if j == 0:
                    it = QListWidgetItem(str(i) + ") " + str(elem[1]))
                    self.listWidget.addItem(it)
                if val[0]:
                    s = QListWidgetItem("✓ " + str(val[1]))
                else:
                    s = QListWidgetItem("- " + str(val[1]))
                self.listWidget.addItem(s)


class Window3(QMainWindow):
    def __init__(self):
        super(Window3, self).__init__()
        uic.loadUi('reshit.ui', self)
        self.setFixedSize(1000, 1000)
        self.con = sqlite3.connect("viktorina.db")
        self.cur = self.con.cursor()
        self.res = self.cur.execute(f'SELECT id, text FROM voprosi').fetchall()
        res1 = self.cur.execute(f'SELECT id FROM otveti').fetchall()
        if len(res1) == 0 or len(self.res) == 0:
            it = QListWidgetItem("Таблица пуста или вы добавили только вопросы без вариантов ответа!")
            self.listWidget.addItem(it)
            self.pushButton_4.hide()
        self.num = 0
        self.balli = 0
        self.vsego = 0
        self.nam = ""
        self.con.commit()
        self.initUI()

    def initUI(self):
        self.pushButton_4.clicked.connect(self.proshel)
        self.pushButton.clicked.connect(self.show_window_2)
        self.pushButton_2.clicked.connect(self.show_window_1)
        self.pushButton_3.clicked.connect(self.show_window_3)

    def proshel(self):
        res1 = []
        if self.num == 0:
            self.prav = []
            self.listWidget.clear()
            if self.lineEdit.text() == "":
                self.listWidget.addItem(QListWidgetItem("Имя не может быть пустым"))
                return
            else:
                self.nam = self.lineEdit.text()
            while not res1:
                res1 = self.cur.execute(
                    f'SELECT pravilno, text FROM otveti WHERE vopros = {self.res[self.num][0]}').fetchall()
                self.con.commit()
                if not res1:
                    self.num += 1
            it = QListWidgetItem(self.res[self.num][1])
            self.num += 1
            self.listWidget.addItem(it)
            n = 1
            for i, j in res1:
                self.prav.append(i)
                it = QListWidgetItem(str(n) + ") " + j)
                n = n + 1
                self.listWidget.addItem(it)
        elif self.num != len(self.res):
            pr = [0] * len(self.prav)
            ids = self.lineEdit_2.text().split()
            for i in ids:
                if i.isdigit() and int(i) <= len(pr):
                    pr[int(i) - 1] = 1
            if pr == self.prav:
                self.balli += 3
                self.lcdNumber.display(self.balli)
            self.vsego += 3
            self.prav.clear()
            self.listWidget.clear()
            while not res1 and self.num != len(self.res):
                res1 = self.cur.execute(
                    f'SELECT pravilno, text FROM otveti WHERE vopros = {self.res[self.num][0]}').fetchall()
                self.con.commit()
                if not res1:
                    self.num += 1
            if self.num == len(self.res):
                self.zakonchil()
            else:
                it = QListWidgetItem(self.res[self.num][1])
                self.num += 1
                self.listWidget.addItem(it)
                n = 1
                for i, j in res1:
                    self.prav.append(i)
                    it = QListWidgetItem(str(n) + ") " + j)
                    n = n + 1
                    self.listWidget.addItem(it)
        else:
            self.shet()
            self.zakonchil()

    def zakonchil(self):
        a1 = (self.cur.execute("""SELECT COUNT(*) FROM rating""").fetchone())[0]
        if a1 == 0:
            ids = 1
        else:
            ids = self.cur.execute("""SELECT MAX(id) FROM rating""").fetchone()[0] + 1
        self.con.commit()
        st = """INSERT INTO rating
                               (id, balli, name, percents, maximum)
                               VALUES (?, ?, ?, ?, ?);"""
        per = str(self.balli / self.vsego)[:3]
        per = str(float(per) * 100) + " %"
        data_tuple = (ids, self.balli, self.nam, per, self.vsego)
        self.cur.execute(st, data_tuple)
        self.con.commit()
        self.listWidget.clear()
        self.listWidget.addItem(QListWidgetItem(f"Вы успешно прошли викторину, количество ваших баллов: {self.balli}"))
        self.balli = 0
        self.vsego = 0
        self.nam = ""
        self.num = 0
        self.lcdNumber.display(self.balli)

    def show_window_2(self):
        self.w2 = MyWidget()
        if self.nam != "":
            self.shet()
            self.zakonchil()
        self.w2.show()
        self.close()

    def show_window_1(self):
        self.w1 = Window1()
        if self.nam != "":
            self.shet()
            self.zakonchil()

        self.w1.show()
        self.close()

    def show_window_3(self):
        self.w3 = Window2()
        if self.nam != "":
            self.shet()
            self.zakonchil()
        self.w3.show()
        self.close()

    def shet(self):
        pr = [0] * len(self.prav)
        ids = self.lineEdit_2.text().split()
        for i in ids:
            if i.isdigit() and int(i) <= len(pr):
                pr[int(i) - 1] = 1
        self.vsego += 3
        if pr == self.prav:
            self.balli += 3
            self.lcdNumber.display(self.balli)


class Pervoe(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("nachalo.ui", self)
        self.setFixedSize(1000, 1000)
        self.pushButton.clicked.connect(self.show_window_2)
        self.pushButton_2.clicked.connect(self.show_window_1)
        self.pushButton_3.clicked.connect(self.show_window_3)
        self.pushButton_4.clicked.connect(self.show_window_4)

    def show_window_2(self):
        self.w2 = MyWidget()
        self.w2.show()
        self.close()

    def show_window_1(self):
        self.w1 = Window2()
        self.w1.show()
        self.close()

    def show_window_3(self):
        self.w3 = Window3()
        self.w3.show()
        self.close()

    def show_window_4(self):
        self.w4 = Window1()
        self.w4.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Pervoe()
    ex.show()
    sys.exit(app.exec_())
