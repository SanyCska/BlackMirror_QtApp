from PyQt5 import QtCore, QtGui, QtWidgets
from time import strftime
from weather import Weather
from threading import Thread #Потоки
from PyQt5.QtCore import QObject, pyqtSignal
from socket import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys

HOST = 'localhost'  # адрес хоста (сервера) пустой означает использование любого доступного адреса
PORT = 21111  # номер порта на котором работает сервер (от 0 до 65525, порты до 1024 зарезервированы для системы, порты TCP и UDP не пересекаются)
BUFSIZ = 1024  # размер буфера 1Кбайт
ADDR = (HOST, PORT)  # адрес сервера
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)  # связываем сокет с адресом
tcpSerSock.listen(5)  # устанавливаем максимальное число клиентов одновременно обслуживаемых

class Ui_Form(object):
    city = ''
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setStyleSheet('background-color: black')
        # Form.resize(1167, 912)
        MainWindow.setWindowState(QtCore.Qt.WindowMaximized)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(360, 110, 181, 181))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Cloud.jpg"))
        self.label.setObjectName("label")
        self.label.hide()

        self.lcdNumber = QtWidgets.QLCDNumber(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(290, 20, 561, 361))
        self.lcdNumber.setStyleSheet('background-color: black;'
                                     'color: white')
        self.lcdNumber.setObjectName("lcdNumber")
        self.hide_lcd()

        self.timer = QtCore.QTimer(Form)
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)

        self.lcd = QtWidgets.QLCDNumber(Form)
        self.lcd.setGeometry(QtCore.QRect(1000, 20, 561, 361))
        self.lcd.setStyleSheet('background-color: black;'
                               'color: white')

        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(340, 300, 261, 200))
        self.textEdit.setReadOnly(True)
        self.textEdit.setStyleSheet('background-color: black;'
                                    'border-style: solid;'
                                    'color: white')
        self.textEdit.setFont(QtGui.QFont('Segoe UI Black', 24))
        self.textEdit.setObjectName("textEdit")
        self.hide_text()

        self.textEdit2 = QtWidgets.QTextEdit(Form)
        self.textEdit2.setGeometry(QtCore.QRect(1000, 300, 1000, 700))
        self.textEdit2.setReadOnly(True)
        self.textEdit2.setStyleSheet('background-color: black;'
                                    'border-style: solid;'
                                    'color: white')
        self.textEdit2.setFont(QtGui.QFont('Segoe UI Black', 12))
        self.textEdit2.setObjectName("textEdit2")
        self.News()

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setStyleSheet('background-color: grey')
        self.pushButton.setGeometry(QtCore.QRect(100, 550, 150, 46))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.pressed.connect(self.show_all)

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(360, 110, 181, 181))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("Rain.jpg"))
        self.label_2.setObjectName("label_2")
        self.label_2.hide()

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(360, 110, 181, 181))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("Sun.jpg"))
        self.label_3.setObjectName("label_3")
        self.label_3.hide()

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(360, 110, 181, 181))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("Snow.jpg"))
        self.label_4.setObjectName("label_4")
        self.label_4.hide()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "PushButton"))

    def hide_lcd(self):
        self.lcdNumber.hide()

    def hide_text(self):
        self.textEdit.hide()

    def city(self, string):
        self.city = string
        print(self.city)

    def Time(self):
        self.lcd.display(strftime("%H"+":"+"%M"))

    def News(self):
        html = urlopen('https://yandex.ru')
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        news = bsObj.div.ol.findAll("a")
        news_list = []
        news_string = ""
        for each in news:
            news_list.append(each.text)
            news_string = news_string + ("● " + each.text + "\n\n")
        self.textEdit2.setText(news_string)

    def show_all(self):
        weather = Weather()
        location = weather.lookup_by_location(self.city)
        condition = location.condition()
        temp = (int(condition.temp()) - 32) * 5 // 9
        self.lcdNumber.display(temp)
        self.lcd.display(strftime("%H" + ":" + "%M"))
        text = str(condition.text())
        print(text)
        if 'loudy' in text:
            self.label.show()
        else:
            if 'now' in text:
                self.label_4.show()
            else:
                if 'ain' in text:
                    self.label_2.show()
                else:
                    if 'unny' or 'lear' in text:
                        self.label_3.show()
                    else:
                        if 'hover' in text:
                            self.label_2.show
        self.textEdit.setText(text)
        self.lcdNumber.show()
        self.textEdit.show()


class MyThread(Thread):
    def __init__(self, f):
        Thread.__init__(self)
        self.f = f

    def run(self):
        tcpCliSock, addr = tcpSerSock.accept()
        print('Connected from: {}'.format(addr))
        while True:
            data = tcpCliSock.recv(BUFSIZ)
            data.decode('utf8')
            if data:
                print(data)
                if data == b'1':
                    self.f.message.emit()
                if data == b'Moscow':
                    self.f.message2.emit('Moscow')

class foo(QObject):
    message = pyqtSignal()
    message2 = pyqtSignal(str)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    f = foo()
    f.message.connect(ui.show_all)
    f.message2.connect(ui.city)
    t = MyThread(f)
    t.start()
    sys.exit(app.exec_())
