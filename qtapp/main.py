from sys import argv, exit
from qtpy import QtWidgets
from PyQt5.Qt import QApplication, QIcon
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5.QtGui import QKeySequence
from ctypes import windll
from ui.mainwindow import Ui_MainWindow
from spellchecker import SpellChecker
import string


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent, flags=Qt.WindowFlags())

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.first_char.textChanged.connect(self.onfirstchange)
        self.ui.second_char.textChanged.connect(self.onsecchange)
        self.ui.third_char.textChanged.connect(self.onthirdchange)
        self.ui.fourth_char.textChanged.connect(self.onfourthchange)
        self.ui.fifth_char.textChanged.connect(self.onfifthchange)

        self.ui.check_btn.clicked.connect(self.oncheckclick)
        self.wordlist = []

        self.spell = SpellChecker(language="de")

        self.possibles = []

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Enter or key == Qt.Key_Return:
            self.oncheckclick()

    def onfirstchange(self):
        self.onstatchange(self.ui.first_char.text(), self.ui.first_char)
        self.ui.second_char.setFocus()

    def onsecchange(self):
        self.onstatchange(self.ui.second_char.text(), self.ui.second_char)
        self.ui.third_char.setFocus()

    def onthirdchange(self):
        self.onstatchange(self.ui.third_char.text(), self.ui.third_char)
        self.ui.fourth_char.setFocus()

    def onfourthchange(self):
        self.onstatchange(self.ui.fourth_char.text(), self.ui.fourth_char)
        self.ui.fifth_char.setFocus()

    def onfifthchange(self):
        self.onstatchange(self.ui.fifth_char.text(), self.ui.fifth_char)
        self.ui.check_btn.setFocus()

    @staticmethod
    def onstatchange(text: str, char: QtWidgets.QLineEdit):
        if text == "":
            char.setStyleSheet("background-color: lightgrey")
        else:
            char.setStyleSheet("background-color: #a0fa55")

    def oncheckclick(self):
        self.possibles.clear()
        self.ui.results_list.clear()

        yellows = self.ui.yellows_edit.text().lower()
        greys = self.ui.greys_edit.text().lower()
        word = self.buildword()

        self.iterate(word, yellows, greys)

        for i in self.possibles:
            self.isaword(i)

    def iterate(self, word, y, g):
        for i in word:
            if i == "_":
                for j in string.ascii_lowercase:
                    newword = word.split("_", 1)[0] + j + word.split("_", 1)[1]
                    self.iterate(newword, y, g)
                    if self.check(newword, y, g):
                        self.possibles.append(newword)
                break

    @staticmethod
    def check(word, y, g):
        valid = False
        # Word has all yellow letters
        if set(y).issubset(word):
            valid = True
        # Word contains not one of the grey letters
        for i in word:
            if i in g:
                valid = False
        # Word is from final iteration without any blanks
        if "_" in word:
            valid = False
        return valid

    def isaword(self, word):
        if word in self.wordlist:
            self.ui.results_list.addItem(word)

    def buildword(self):
        word = ""
        if self.ui.first_char.text():
            word = word + self.ui.first_char.text().lower()
        else:
            word = word + "_"

        if self.ui.second_char.text():
            word = word + self.ui.second_char.text().lower()
        else:
            word = word + "_"

        if self.ui.third_char.text():
            word = word + self.ui.third_char.text().lower()
        else:
            word = word + "_"

        if self.ui.fourth_char.text():
            word = word + self.ui.fourth_char.text().lower()
        else:
            word = word + "_"

        if self.ui.fifth_char.text():
            word = word + self.ui.fifth_char.text().lower()
        else:
            word = word + "_"
        return word


class AppIcon(QIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addFile('data/ico/logo16.png', QSize(16, 16))
        self.addFile('data/ico/logo24.png', QSize(24, 24))
        self.addFile('data/ico/logo32.png', QSize(32, 32))
        self.addFile('data/ico/logo48.png', QSize(48, 48))


if __name__ == '__main__':
    app = QApplication(argv)

    myappid = 'wordlehelper'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app_icon = AppIcon()
    app.setWindowIcon(app_icon)

    mainwindow = MainWindow()

    with open("newdict.txt", "r") as f:
        mainwindow.wordlist = f.read().splitlines()

    mainwindow.show()

    exit(app.exec_())
