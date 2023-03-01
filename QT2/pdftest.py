from PyQt5.QtCore import  QIODevice, QFile, Qt, QMarginsF, QRect
from PyQt5.QtGui import  QPagedPaintDevice, QPdfWriter, QPainter,QFont
from PyQt5.QtWidgets import QWidget,QApplication

class PdfWrite(QWidget):
    """docstring for PdfWrite"""
    def __init__(self, *arg):
        super(PdfWrite, self).__init__(*arg)

    def writePdf(self, name):
        pdfFile = QFile(name)
        #打开要写入的pdf文件
        pdfFile.open(QIODevice.WriteOnly)

        #创建pdf写入器
        pPdfWriter = QPdfWriter(pdfFile)
        #设置纸张为A4
        pPdfWriter.setPageSize(QPagedPaintDevice.A4)
        #设置纸张的分辨率为300,因此其像素为3508X2479
        pPdfWriter.setResolution(300)
        pPdfWriter.setPageMargins(QMarginsF(60, 60, 60, 60))

        pPdfPainter = QPainter(pPdfWriter)

        # 标题上边留白
        iTop = 100

        #文本宽度2100
        iContentWidth = 2100

        # 标题,22号字
        font = QFont()
        font.setFamily("simhei.ttf")
        fontSize = 22
        font.setPointSize(fontSize)

        pPdfPainter.setFont(font)
        pPdfPainter.drawText(QRect(0, iTop, iContentWidth, 90), Qt.AlignHCenter, "我是标题我骄傲")

        # 内容,16号字，左对齐
        fontSize = 16
        font.setPointSize(fontSize)
        pPdfPainter.setFont(font)

        iTop += 90
        pPdfPainter.drawText(QRect(0, iTop, iContentWidth, 60), Qt.AlignLeft, "1、目录一")
        iTop += 90
        # 左侧缩进2字符
        iLeft = 120
        pPdfPainter.drawText(QRect(iLeft, iTop, iContentWidth - iLeft, 60), Qt.AlignLeft, "我的目录一的内容。")
        iTop += 90
        pPdfPainter.drawText(QRect(0, iTop, iContentWidth, 60), Qt.AlignLeft, "2、目录二")
        iTop += 90
        pPdfPainter.drawText(QRect(iLeft, iTop, iContentWidth - iLeft, 60), Qt.AlignLeft, "我的目录一的内容")

        pPdfPainter.end()
        pdfFile.close()

if __name__ == '__main__':

    import sys
    from PyQt5.QtWidgets import QFileDialog

    app = QApplication(sys.argv)
    pWrite = PdfWrite()
    #pWrite.show()
    name = QFileDialog.getSaveFileName(None, "Save File",
                            "123.pdf", "*.pdf")
    if name[0]:
        print(name[0])
        pWrite.writePdf(name[0])
    else:
        pWrite.close()
    sys.exit(app.exec_())