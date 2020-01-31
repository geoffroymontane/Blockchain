import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLineEdit, QLabel, QDesktopWidget, QMessageBox
import time
from PyQt5.QtCore import *
# For passing the string to some function in another file:
from StringStorage import *
from client_test import *

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'CopyRight Register'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 480
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.AuthorLabel = QLabel(self)
        self.AuthorLabel.setText('Name:')
        self.Authortextbox = QLineEdit(self)
        self.AuthorLabel.move(30,102)
        self.Authortextbox.move(70, 100)
        self.Authortextbox.resize(280,20)

        #File Name
        self.FileLabel = QLabel(self)
        self.FileLabel.setText('File:')
        self.Filetextbox = QLineEdit(self)
        self.FileLabel.move(30,202)
        self.Filetextbox.move(70, 200)
        self.Filetextbox.resize(280,20)

        #File type
        self.TypeLabel = QLabel(self)
        self.TypeLabel.setText('Type:')
        self.Typetextbox = QLineEdit(self)
        self.TypeLabel.move(30,302)
        self.Typetextbox.move(70, 300)
        self.Typetextbox.resize(280,20)

        # Create a button in the window
        self.buttonSave = QPushButton('Save', self)
        self.buttonSave.move(75, 400)

        self.buttonverify = QPushButton('Verify', self)
        self.buttonverify.move(275, 400)

        # When the 'clicked' signal of the button is emitted, call some function (which acts as a slot):
        self.buttonSave.clicked.connect(self.onButtonClicked)
        self.buttonverify.clicked.connect(self.verify)
        self.show()

        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = (ag.width() - widget.width())/2
        y = 2 * ag.height() - sg.height() - widget.height() - 100
        self.move(x, y)

    # Function to pass the entered string along to the function from another file
    def onButtonClicked(self):
        storeString1(self.Authortextbox.text())
        storeString2(self.Filetextbox.text())
        storeString3(self.Typetextbox.text())
        run()

    def verify(self):
        storeString1(self.Authortextbox.text())
        storeString2(self.Filetextbox.text())
        storeString3(self.Typetextbox.text())
        text = verification()
        msg = QMessageBox()
        msg.setWindowTitle("Verfication")
        msg.setText(text)
        x = msg.exec_()  # this will show our messagebox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

