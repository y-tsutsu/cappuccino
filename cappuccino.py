import sys, os
from downloader import download_image
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF, QMargins

dirname  = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'image')

def download():
    keyword = '美女'
    minsize = (500, 500)
    download_image(keyword, 100, dirname, minsize)

class ImageViewScene(QGraphicsScene):
    def __init__(self, *argv, **keywords):
        super(ImageViewScene, self).__init__(*argv, **keywords)

class ImageView(QGraphicsView):
    def __init__(self, parent = None):
        super(ImageView, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        scene = ImageViewScene(self)
        scene.setSceneRect(QRectF(self.rect()))
        self.setScene(scene)

        self.resizeEvent = self.on_resize

        self.resize(500, 500)
        self.setWindowTitle("cappuccino")

    def on_resize(self, event):
        super(ImageView, self).resizeEvent(event)
        print(self.width(), self.height())

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent, Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.init_ui()

    def init_ui(self):
        view = ImageView(self)
        view.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        layout = QHBoxLayout()
        layout.addWidget(view)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(layout)

        self.resize(500, 500)
        self.setWindowTitle("cappuccino")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
