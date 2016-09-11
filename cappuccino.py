import sys, os, random, threading
from downloader import Downloader
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QHBoxLayout, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtGui import QPixmap, QPainter, QImage, QMouseEvent
from PyQt5.QtCore import Qt, QMargins, QRectF, QTimer, QSize, QPoint, pyqtSignal

DIR_NAME  = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'image')

DOUNLOAD_COUNT = 100

IMAGE_INTERVAL = 20000

DEFAULT_KEYWORD = 'ねこ'

class ImageView(QGraphicsView):
    mouse_left_press = pyqtSignal(QPoint)
    mouse_left_move = pyqtSignal(QPoint)
    mouse_left_release = pyqtSignal(QPoint)
    mouse_double_click = pyqtSignal(QMouseEvent)

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
        super(ImageView, self).mousePressEvent(event)
        if (event.button() == Qt.LeftButton):
            self.__is_mouse_left_press = True
            pos = self.point_to_parent(event.pos())
            self.mouse_left_press.emit(pos)

    def mouseMoveEvent(self, event):
        super(ImageView, self).mouseMoveEvent(event)
        if (self.__is_mouse_left_press):
            pos = self.point_to_parent(event.pos())
            self.mouse_left_move.emit(pos)

    def mouseReleaseEvent(self, event):
        super(ImageView, self).mouseReleaseEvent(event)
        if (event.button() == Qt.LeftButton):
            self.__is_mouse_left_press = False
            pos = self.point_to_parent(event.pos())
            self.mouse_left_release.emit(pos)

    def mouseDoubleClickEvent(self, event):
        super(ImageView, self).mouseDoubleClickEvent(event)
        self.mouse_double_click.emit(event)

class MainWindow(QWidget):
    complete_progress = pyqtSignal()

    def __init__(self, download_keyword, parent = None):
        super(MainWindow, self).__init__(parent, Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.__download_keyword = download_keyword
        self.complete_progress.connect(self.on_complete_progress)

        # download
        self.__download_label = None
        self.__downloader = None
        self.__progress_bar = None

        # image
        self.__view = None
        self.__timer = None
        self.__image_list = None
        self.__mouse_left_press_pos = None

        if self.__download_keyword:
            self.init_download_ui()
        else:
            self.init_image_ui()

        self.start()

    def init_common_ui(self):
        self.resize(500, 300)
        self.setWindowTitle("cappuccino")

        if not self.layout():
            vbox = QVBoxLayout(self)
            self.setLayout(vbox)

    def init_download_ui(self):
        self.init_common_ui()

        self.__download_label = QLabel('カプチーノを入れています．．．', self)
        self.__download_label.setAlignment(Qt.AlignCenter)

        self.__progress_bar = QProgressBar(self)
        self.__progress_bar.setRange(0, DOUNLOAD_COUNT)
        self.__progress_bar.setTextVisible(False)

        layout = self.layout()
        layout.addWidget(self.__download_label)
        layout.addWidget(self.__progress_bar)
        layout.setContentsMargins(QMargins(16, 16, 16, 16))

        self.__downloader = Downloader()
        self.__downloader.progress_download.connect(self.on_progress_download)

    def init_image_ui(self):
        self.init_common_ui()

        self.__view = ImageView(self)

        layout = self.layout()
        layout.removeWidget(self.__download_label)
        layout.removeWidget(self.__progress_bar)
        layout.addWidget(self.__view)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))

        self.__view.mouse_left_press.connect(self.on_view_mouse_left_press)
        self.__view.mouse_left_move.connect(self.on_view_mouse_left_move)
        self.__view.mouse_left_release.connect(self.on_view_mouse_left_release)
        self.__view.mouse_double_click.connect(self.on_view_mouse_double_click)

        self.__timer = QTimer(self)
        self.__timer.setInterval(IMAGE_INTERVAL)
        self.__timer.timeout.connect(self.on_timeout)

    def init_image_list(self):
        self.__image_list = [x for x in os.listdir(DIR_NAME) if os.path.isfile(os.path.join(DIR_NAME, x))]

    def start(self):
        if self.__download_keyword:
            th = threading.Thread(target = self.download, args = (self.__download_keyword, ))
            th.start()
        else:
            self.init_image_list()
            self.random_set_image()
            self.__timer.start()

    # ダウンロード関連

    def download(self, keyword):
        minsize = (300, 300)
        self.__downloader.download_image(keyword, DOUNLOAD_COUNT, DIR_NAME, minsize)
        self.complete_progress.emit()

    def on_progress_download(self, progress):
        self.__progress_bar.setValue(progress)

    def on_complete_progress(self):
        self.__download_keyword = ''
        self.init_image_ui()
        self.start()

    # 表示関連

    def random_set_image(self):
        image = random.choice(self.__image_list)
        self.__image_list.remove(image)
        self.__view.set_image(os.path.join(DIR_NAME, image))

    def on_timeout(self):
        if not self.__image_list:
            self.init_image_list()
        self.random_set_image()

    # ウィンドウ移動関連

    def point_to_screen(self, pos):
        return QPoint(self.x() + pos.x(), self.y() + pos.y())

    def on_view_mouse_left_press(self, pos):
        self.__mouse_left_press_pos = pos
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def on_view_mouse_left_move(self, pos):
        if not self.__mouse_left_press_pos:
            return
        screen_pos = self.point_to_screen(pos)
        self.move(QPoint(screen_pos.x() - self.__mouse_left_press_pos.x(), screen_pos.y() - self.__mouse_left_press_pos.y()))

    def on_view_mouse_left_release(self, pos):
        self.__mouse_left_press_pos = None

    def on_view_mouse_double_click(self, event):
        self.setWindowState(Qt.WindowMinimized)

    def mousePressEvent(self, event):
        super(MainWindow, self).mousePressEvent(event)
        if (event.button() == Qt.LeftButton):
            self.on_view_mouse_left_press(event.pos())

    def mouseMoveEvent(self, event):
        super(MainWindow, self).mouseMoveEvent(event)
        self.on_view_mouse_left_move(event.pos())

    def mouseReleaseEvent(self, event):
        super(MainWindow, self).mouseReleaseEvent(event)
        if (event.button() == Qt.LeftButton):
            self.on_view_mouse_left_release(event.pos())

    def mouseDoubleClickEvent(self, event):
        super(MainWindow, self).mouseDoubleClickEvent(event)
        self.on_view_mouse_double_click(event)

def main():
    app = QApplication(sys.argv)
    download_keyword = sys.argv[1] if (2 <= len(sys.argv)) else ''
    if not download_keyword and not os.path.isdir(DIR_NAME):
        download_keyword = DEFAULT_KEYWORD

    window = MainWindow(download_keyword)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
