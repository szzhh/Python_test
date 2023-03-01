import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QWidget()
    win.resize(1000, 800)
    win.move(300, 300)
    win.setWindowTitle('Hello World')
    win.show()
    sys.exit(app.exec_())