# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fileupload.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

fileupload_ui = r'fileupload.ui'

class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(fileupload_ui, self)

        self.pushButton.clicked.connect(self.Button_click)

    def Button_click(self):
        file_names = QFileDialog.getOpenFileNames(self)

        for file in file_names[0]:
            exist = self.textEdit.toPlainText()
            self.textEdit.setText(exist + file + '\n')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Dialog = MainDialog()
    Dialog.show()
    app.exec_()
