from PyQt5.Qt import *
import sys

app = QApplication(sys.argv)

w = QWidget()
w.setWindowTitle("QButtonGrounp")
w.resize(300, 150)

#创建第1组 QRadioButton 按钮
cs1 = QRadioButton("特大杯",w)
cs1.move(80, 20)

cs2 = QRadioButton("大杯",w)
cs2.move(80, 40)

cs3 = QRadioButton("中杯",w)
cs3.move(80, 60)

cs4 = QRadioButton("小杯",w)
cs4.move(80, 80)


drs1 = QRadioButton("咖啡",w)
drs1.move(20, 20)

drs2 = QRadioButton("可乐",w)
drs2.move(20, 40)

drs3 = QRadioButton("豆浆",w)
drs3.move(20, 60)


w.show()

if __name__ == '__main__':
    sys.exit(app.exec_())
