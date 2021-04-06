import sys
from PyQt5.QtWidgets import *


class File_upload(QWidget):
    def __init__(self) -> object:
        super().__init__()
        self.pushButton = QPushButton("파일 업로드")
        self.label = QLabel()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("PyStock v0.1")

        self.pushButton.clicked.connect(self.pushButtonClicked)

        layout = QVBoxLayout()
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label.setText(fname[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = File_upload()
    win.show()
    app.exec_()
