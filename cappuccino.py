import sys, os
from downloader import download_image
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import Qt, QMargins

dirname  = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'image')

def download():
    keyword = '美女'
    minsize = (500, 500)
    download_image(keyword, 100, dirname, minsize)

class ImageView(QGraphicsView):
    def __init__(self, parent = None):
        super(ImageView, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.__image = None
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

    def paintEvent(self, event):
        if not self.__image:
            return
        painter = QPainter(self.viewport())
        rect = self.rect()
        painter.drawImage(rect, self.__image)

    def set_image(self, filename):
        self.__image = QImage(filename)

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent, Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.init_ui()

    def init_ui(self):
        view = ImageView(self)
        view.set_image(os.path.join(dirname, 'img21.jpg'))

        hbox = QHBoxLayout()
        hbox.addWidget(view)
        hbox.setContentsMargins(QMargins(0, 0, 0, 0))

        self.setLayout(hbox)

        self.resize(500, 500)
        self.setWindowTitle("cappuccino")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
