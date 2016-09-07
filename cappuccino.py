import sys, os, random
from downloader import download_image
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import Qt, QMargins, QRectF, QTimer, QSize, QPoint, pyqtSignal

dirname  = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'image')

def download():
    keyword = '美人'
    minsize = (500, 500)
    download_image(keyword, 100, dirname, minsize)

class ImageView(QGraphicsView):
    mouse_left_press = pyqtSignal(QPoint)
    mouse_left_move = pyqtSignal(QPoint)
    mouse_left_release = pyqtSignal(QPoint)

    def __init__(self, parent = None):
        super(ImageView, self).__init__(parent)
        self.__image = None
        self.__is_mouse_left_press = False
        self.init_ui()

    def init_ui(self):
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

    def set_image(self, filename):
        self.__image = QImage(filename)
        self.setUpdatesEnabled(False)   # ステータスを書き換えないとrepaint()が効かなかった対策．もっとまともな手はないか．．．
        self.setUpdatesEnabled(True)
        self.repaint()

    def point_to_parent(self, pos):
        return QPoint(self.x() + pos.x(), self.y() + pos.y())

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

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.__is_mouse_left_press = True
            pos = self.point_to_parent(event.pos())
            self.mouse_left_press.emit(pos)

    def mouseMoveEvent(self, event):
        if (self.__is_mouse_left_press):
            pos = self.point_to_parent(event.pos())
            self.mouse_left_move.emit(pos)

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.__is_mouse_left_press = False
            pos = self.point_to_parent(event.pos())
            self.mouse_left_release.emit(pos)

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent, Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.__view = ImageView(self)
        self.__timer = QTimer(self)
        self.__image_list = None
        self.__mouse_left_press_pos = None
        self.init_ui()

    def init_ui(self):
        self.__timer.setInterval(20000)
        self.__timer.timeout.connect(self.on_timeout)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.__view)
        hbox.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(hbox)

        self.resize(500, 300)
        self.setWindowTitle("cappuccino")

        self.__view.mouse_left_press.connect(self.on_view_mouse_left_press)
        self.__view.mouse_left_move.connect(self.on_view_mouse_left_move)
        self.__view.mouse_left_release.connect(self.on_view_mouse_left_release)

        self.init_image_list()
        self.random_set_image()
        self.__timer.start()

    def init_image_list(self):
        self.__image_list = [x for x in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, x))]

    def random_set_image(self):
        image = random.choice(self.__image_list)
        self.__image_list.remove(image)
        self.__view.set_image(os.path.join(dirname, image))

    def point_to_screen(self, pos):
        return QPoint(self.x() + pos.x(), self.y() + pos.y())

    def on_timeout(self):
        if not self.__image_list:
            self.init_image_list()
        self.random_set_image()

    def on_view_mouse_left_press(self, pos):
        self.__mouse_left_press_pos = pos

    def on_view_mouse_left_move(self, pos):
        if not self.__mouse_left_press_pos:
            return
        screen_pos = self.point_to_screen(pos)
        self.move(QPoint(screen_pos.x() - self.__mouse_left_press_pos.x(), screen_pos.y() - self.__mouse_left_press_pos.y()))

    def on_view_mouse_left_release(self, pos):
        self.__mouse_left_press_pos = None

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
