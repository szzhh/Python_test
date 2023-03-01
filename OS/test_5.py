import sys
from PyQt5.QtCore import QTimer, Qt, QRectF
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QColor, QFont, QPainter


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.stopwatch()

    def stopwatch(self):
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        self.setWindowTitle("Example")
        self.setGeometry(400,400,400,200)
        self.formato = "0:00.0"
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_rect(event, qp)
        qp.end()

    def draw_rect(self,event, qp):
        # Black Rectangle
        col = QColor("Black")
        col.setNamedColor("Black")
        qp.setPen(col)
        qp.setBrush(QColor("Black"))
        qp.drawRect(130,000,400,200)
        # formato
        qp.setPen(QColor("Green"))
        qp.setFont(QFont('Helvetica', 48))
        qp.drawText(event.rect(), QRect(50, 50, 50, 50),5 , self.formato)  # Problem 


app = QApplication(sys.argv)
w = Window()