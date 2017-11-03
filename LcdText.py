from PyQt5 import QtCore, QtGui, QtWidgets
from weather import Weather
import sys

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1070, 829)
        self.lcdNumber = QtWidgets.QLCDNumber(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(450, 30, 321, 251))
        self.lcdNumber.setObjectName("lcdNumber")
        self.hide_lcd()


        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(780, 100, 231, 101))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.hide_text()


        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(40, 690, 181, 81))
        self.pushButton.setObjectName("PushButton")
        self.pushButton.pressed.connect(self.show_all)

        self.load_weather()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Show Weather"))

    def hide_lcd(self):
        self.lcdNumber.hide()

    def hide_text(self):
        self.textEdit.hide()

    def show_all(self):
        self.lcdNumber.show()
        self.textEdit.show()

    def load_weather(self):
        weather = Weather()
        location = weather.lookup_by_location('Moscow')
        condition = location.condition()
        temp = (int(condition['temp']) - 32) * 5 // 9
        self.lcdNumber.display(temp)
        text = str(condition['text'])
        self.textEdit.setText(text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
