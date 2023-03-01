import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import Qt

class Drawing(QWidget):
    def __init__(self):
        super().__init__() 
        self.setGeometry(300, 300, 365, 600)
        #self.setWindowTitle('brush')        
        #self.show()

    def paintEvent(self, e): 
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp): 
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor('lightgreen'))
        qp.setBrush(brush)
        qp.drawRect(10, 15, 150, 50)
        qp.setPen(QColor("black"))
        qp.setFont(QFont('Helvetica', 10))
        qp.drawText(100,50,'Hello')

        brush = QBrush(Qt.Dense1Pattern)
        qp.setBrush(brush)
        qp.drawRect(10, 65, 150, 50)

        brush = QBrush(QColor(0, 170, 255),Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 115, 150, 50)

        brush = QBrush(Qt.Dense3Pattern)
        qp.setBrush(brush)
        qp.drawRect(10, 165, 150, 50)

        brush = QBrush(Qt.DiagCrossPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 215, 150, 50)

        brush = QBrush(Qt.Dense5Pattern)
        qp.setBrush(brush)
        qp.drawRect(10, 265, 150, 50)

        brush = QBrush(Qt.Dense6Pattern)
        qp.setBrush(brush)
        qp.drawRect(10, 315, 150, 50)

        brush = QBrush(Qt.HorPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 365, 150, 50)

        brush = QBrush(Qt.VerPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 415, 150, 50)

        brush = QBrush(QColor(0, 170, 255),Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 475, 150, 10)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Drawing()
    demo.show()
    sys.exit(app.exec_())