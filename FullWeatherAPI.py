from PyQt5 import QtCore, QtGui, QtWidgets
from weather import Weather
import sys

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setStyleSheet('background-color: black')
        Form.resize(1167, 912)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(860, 110, 181, 181))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../Downloads/Pic/Cloud.jpg"))
        self.label.setObjectName("label")
        self.label.hide()

        self.lcdNumber = QtWidgets.QLCDNumber(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(290, 20, 561, 361))
        self.lcdNumber.setStyleSheet('background-color: black;'
                                     'color: white')
        self.lcdNumber.setObjectName("lcdNumber")
        self.hide_lcd()

        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(840, 300, 261, 200))
        self.textEdit.setReadOnly(True)
        self.textEdit.setStyleSheet('background-color: black;'
                                    'border-style: solid;'
                                    'color: white')
        self.textEdit.setFont(QtGui.QFont('Segoe UI Black', 24))
        self.textEdit.setObjectName("textEdit")
        self.hide_text()

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setStyleSheet('background-color: grey')
        self.pushButton.setGeometry(QtCore.QRect(10, 850, 150, 46))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.pressed.connect(self.show_all)

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(860, 110, 181, 181))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../../Downloads/Pic/Rain.jpg"))
        self.label_2.setObjectName("label_2")
        self.label_2.hide()

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(860, 110, 181, 181))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("../../Downloads/Pic/Sun.jpg"))
        self.label_3.setObjectName("label_3")
        self.label_3.hide()

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(860, 110, 181, 181))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("../../Downloads/Pic/Snow.jpg"))
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

    def show_all(self):
        weather = Weather()
        location = weather.lookup_by_location('Moscow')
        condition = location.condition()
        temp = (int(condition['temp']) - 32) * 5 // 9
        self.lcdNumber.display(temp)
        text = str(condition['text'])
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


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
