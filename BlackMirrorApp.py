from PyQt5 import QtCore, QtGui, QtWidgets
from time import strftime
from weather import Weather
from threading import Thread #Потоки
from PyQt5.QtCore import QObject, pyqtSignal, QTime
from socket import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys

HOST = 'localhost'  # адрес хоста (сервера) пустой означает использование любого доступного адреса
PORT = 21111  # номер порта на котором работает сервер
BUFSIZ = 1024  # размер буфера 1Кбайт
ADDR = (HOST, PORT)  # адрес сервера
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)  # связываем сокет с адресом
tcpSerSock.listen(5)  # устанавливаем максимальное число клиентов одновременно обслуживаемых

class Ui_MainWindow(object):
    city = ''
    greeting = 'Welcome to our app'
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setStyleSheet('background-color: black')
        MainWindow.resize(1847, 1513)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.Snow = QtWidgets.QLabel(self.centralwidget)
        self.Snow.setGeometry(QtCore.QRect(610, 110, 181, 181))
        self.Snow.setText("")
        self.Snow.setPixmap(QtGui.QPixmap("Snow.jpg"))
        self.Snow.setObjectName("Snow")
        self.Snow.hide()

        self.Sun = QtWidgets.QLabel(self.centralwidget)
        self.Sun.setGeometry(QtCore.QRect(610, 110, 181, 181))
        self.Sun.setText("")
        self.Sun.setPixmap(QtGui.QPixmap("Sun.jpg"))
        self.Sun.setObjectName("Sun")
        self.Sun.hide()

        self.Cloud = QtWidgets.QLabel(self.centralwidget)
        self.Cloud.setGeometry(QtCore.QRect(610, 110, 181, 181))
        self.Cloud.setText("")
        self.Cloud.setPixmap(QtGui.QPixmap("Cloud.jpg"))
        self.Cloud.setObjectName("Cloud")
        self.Cloud.hide()

        self.Rain = QtWidgets.QLabel(self.centralwidget)
        self.Rain.setGeometry(QtCore.QRect(610, 110, 181, 181))
        self.Rain.setText("")
        self.Rain.setPixmap(QtGui.QPixmap("Rain.jpg"))
        self.Rain.setObjectName("Rain")
        self.Rain.hide()

        self.TempLCD = QtWidgets.QLCDNumber(self.centralwidget)
        self.TempLCD.setGeometry(QtCore.QRect(-100, -10, 681, 451))
        self.TempLCD.setStyleSheet('background-color: black;'
                                   'color: white')
        self.TempLCD.setObjectName("TempLCD")
        self.TempLCD.hide()

        self.ClockLCD = QtWidgets.QLCDNumber(self.centralwidget)
        self.ClockLCD.setGeometry(QtCore.QRect(1080, -10, 681, 451))
        self.ClockLCD.setStyleSheet('background-color: black;'
                                    'color: white')
        self.ClockLCD.setObjectName("ClockLDC")
        self.ClockLCD.hide()

        self.Welcome = QtWidgets.QTextEdit(self.centralwidget)
        self.Welcome.setGeometry(QtCore.QRect(QtCore.QRect(1230, 450, 531, 991)))
        self.Welcome.setReadOnly(True)
        self.Welcome.setStyleSheet('background-color: black;'
                                'border-style: solid;'
                                'color: white')
        self.Welcome.setFont(QtGui.QFont('Segoe UI Black', 18))
        self.Welcome.setObjectName("Welcome")
        self.Welcome.hide()
        #
        # self.Schedule = QtWidgets.QTextEdit(self.centralwidget)
        # self.Schedule.setGeometry(QtCore.QRect(1230, 450, 531, 991))
        # self.Schedule.setReadOnly(True)
        # self.Schedule.setStyleSheet('background-color: black;'
        #                         'border-style: solid;'
        #                         'color: white')
        # self.Schedule.setFont(QtGui.QFont('Segoe UI Black', 12))
        # self.Schedule.setObjectName("Schedule")

        self.Weather = QtWidgets.QTextEdit(self.centralwidget)
        self.Weather.setGeometry(QtCore.QRect(600, 300, 300, 100))
        self.Weather.setReadOnly(True)
        self.Weather.setStyleSheet('background-color: black;'
                                    'border-style: solid;'
                                    'color: white')
        self.Weather.setFont(QtGui.QFont('Segoe UI Black', 22))
        self.Weather.setObjectName("Weather")

        self.News = QtWidgets.QTextEdit(self.centralwidget)
        self.News.setGeometry(QtCore.QRect(310, 450, 811, 981))
        self.News.setReadOnly(True)
        self.News.setStyleSheet('background-color: black;'
                                'border-style: solid;'
                                'color: white')
        self.News.setFont(QtGui.QFont('Segoe UI Black', 12))
        self.News.setObjectName("News")
        self.News.hide()

        self.timer = QtCore.QTimer(MainWindow)
        self.timer.timeout.connect(self.getTime)
        self.timer.start(1000)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1847, 38))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.getWelcome()
        self.getNews()
        self.getTime()
        self.showWeather()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def getTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]

        self.ClockLCD.display(text)
        self.ClockLCD.show()

    def getNews(self):
        html = urlopen('https://yandex.ru')
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        news = bsObj.div.ol.findAll("a")
        news_list = []
        news_string = ""
        for each in news:
            news_list.append(each.text)
            news_string = news_string + ("● " + each.text + "\n\n")
        self.News.setText(news_string)
        self.News.show()

    def getWelcome(self):

        self.Welcome.setText(self.greeting)
        self.Welcome.show()

    def showWeather(self):
        weather = Weather()
        location = weather.lookup_by_location('Moscow')
        condition = location.condition()
        temp = (int(condition.temp()) - 32) * 5 // 9
        self.TempLCD.display(temp)
        self.ClockLCD.display(strftime("%H" + ":" + "%M"))
        text = str(condition.text())
        if 'loudy' in text:
            self.Cloud.show()
        else:
            if 'now' in text:
                self.Snow.show()
            else:
                if 'ain' in text:
                    self.Rain.show()
                else:
                    if 'unny' or 'lear' in text:
                        self.Sun.show()
                    else:
                        if 'hover' in text:
                            self.Rain.show
        self.Weather.setText(text)
        self.TempLCD.show()
        self.Weather.show()

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
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showFullScreen()
    # f = foo()
    # f.message.connect(ui.showWeather)
    # f.message2.connect(ui.city)
    # t = MyThread(f)
    # t.start()
    sys.exit(app.exec_())
