import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLineEdit, QLabel
# For passing the string to some function in another file:
from StringStorage import *
#from client import *

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'CopyRight Register'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.AuthorLabel = QLabel(self)
        self.AuthorLabel.setText('Name:')
        self.Authortextbox = QLineEdit(self)
        self.AuthorLabel.move(10,102)
        self.Authortextbox.move(50, 100)
        self.Authortextbox.resize(280,20)

        #File Name
        self.FileLabel = QLabel(self)
        self.FileLabel.setText('File:')
        self.Filetextbox = QLineEdit(self)
        self.FileLabel.move(10,202)
        self.Filetextbox.move(50, 200)
        self.Filetextbox.resize(280,20)

        #File type
        self.TypeLabel = QLabel(self)
        self.TypeLabel.setText('Type:')
        self.Typetextbox = QLineEdit(self)
        self.TypeLabel.move(10,302)
        self.Typetextbox.move(50, 300)
        self.Typetextbox.resize(280,20)

        # Create a button in the window
        self.button = QPushButton('Run', self)
        self.button.move(300, 400)

        # When the 'clicked' signal of the button is emitted, call some function (which acts as a slot):
        self.button.clicked.connect(self.onButtonClicked)

        self.show()

    # Function to pass the entered string along to the function from another file
    def onButtonClicked(self):
        storeString1(self.Authortextbox.text())
        storeString2(self.Filetextbox.text())
        storeString3(self.Typetextbox.text())

#if __name__ == '__main__':
def get_values():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
