from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit, QMessageBox
from PySide2 import QtWidgets

class Stats():
    def __init__(self):
        self.window = QMainWindow()
        self.window.resize(1000, 800)
        self.window.move(300, 300)
        self.window.setWindowTitle('薪资统计')

        self.textEdit = QPlainTextEdit(self.window)
        self.textEdit.setPlaceholderText("请输入薪资表")
        self.textEdit.move(20, 25)
        self.textEdit.resize(700, 600)
        self.lineEdit = QPlainTextEdit(self.window)
        self.lineEdit.setPlaceholderText("请输入文件路径")
        self.lineEdit.move(20, 690)
        self.lineEdit.resize(700, 50)

        self.button = QPushButton('统计', self.window)
        self.button.move(800, 300)
        
        self.button1 = QPushButton('浏览',self.window)
        self.button1.move(800, 700)

        self.button.clicked.connect(self.handleCalc)
        self.button1.clicked.connect(self.setBrowerPath)


    def handleCalc(self):
        info = self.textEdit.toPlainText()

        # 薪资20000 以上 和 以下 的人员名单
        salary_above_20k = ''
        salary_below_20k = ''
        for line in info.splitlines():
            if not line.strip():
                continue
            parts = line.split(' ')
            # 去掉列表中的空字符串内容
            parts = [p for p in parts if p]
            name,salary,age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'

        QMessageBox.about(self.window,
                    '统计结果',
                    f'''薪资20000 以上的有：\n{salary_above_20k}
                    \n薪资20000 以下的有：\n{salary_below_20k}'''
                    )
    def setBrowerPath(self):
        download_path = QtWidgets.QFileDialog.getOpenFileName(None,'浏览','D:')
        self.lineEdit.setPlainText(download_path[0])
        print(download_path[0])


app = QApplication([])
stats = Stats()
stats.window.show()
app.exec_()