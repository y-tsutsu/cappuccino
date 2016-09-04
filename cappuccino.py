import sys, os
from downloader import download_image
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsPixmapItem
from PyQt5.QtCore import Qt

def download():
    keyword = '美女'
    dirname  = os.path.join(os.path.dirname(__file__), 'image')
    minsize = (500, 500)
    download_image(keyword, 100, dirname, minsize)

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent, Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.resize(500, 500)
        self.setWindowTitle("cappuccino")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    download()
