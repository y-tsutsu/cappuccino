import sys, os, random
from downloader import download_image
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QImage, QTransform
from PyQt5.QtCore import Qt, QMargins, QRectF, QTimer, QSize

dirname  = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'image')

def download():
    keyword = '美女'
    minsize = (500, 500)
    download_image(keyword, 100, dirname, minsize)

class ImageView(QGraphicsView):
    def __init__(self, parent = None):
        super(ImageView, self).__init__(parent)
        self.__image = None
        self.init_ui()

    def init_ui(self):
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

    def set_image(self, filename):
        self.__image = QImage(filename)
        self.setUpdatesEnabled(False)   # ステータスを書き換えないとrepaint()が効かなかった対策．もっとまともな手はないか．．．
        self.setUpdatesEnabled(True)
        self.repaint()

    def paintEvent(self, event):
        if not self.__image:
            return

        if self.__image.height() == 0 or self.height() == 0 or self.__image.width() == 0:
            return

        image_aspect_ratio = self.__image.width() / self.__image.height()
        view_aspect_ratio = self.width() / self.height()
        if view_aspect_ratio <= image_aspect_ratio:
            image_height = self.width() / image_aspect_ratio
            rect = QRectF(0, (self.height() - image_height) / 2, self.width(), image_height)
        else:
            image_widh = self.height() * image_aspect_ratio
            rect = QRectF((self.width() - image_widh) / 2, 0, image_widh, self.height())

        painter = QPainter(self.viewport())
        painter.drawImage(rect, self.__image)
        painter.end()

        super(ImageView, self).paintEvent(event)

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent, Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.__view = ImageView(self)
        self.__timer = QTimer(self)
        self.__image_list = None
        self.init_ui()

    def init_ui(self):
        self.__timer.setInterval(1000)
        self.__timer.timeout.connect(self.on_timeout)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.__view)
        hbox.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(hbox)

        self.resize(500, 300)
        self.setWindowTitle("cappuccino")

        self.init_image_list()
        self.__timer.start()

    def init_image_list(self):
        self.__image_list = [x for x in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, x))]

    def random_set_image(self):
        image = random.choice(self.__image_list)
        self.__image_list.remove(image)
        self.__view.set_image(os.path.join(dirname, image))

    def on_timeout(self):
        if not self.__image_list:
            self.init_image_list()
        self.random_set_image()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
