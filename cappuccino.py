import sys, os, random, threading
from downloader import Downloader
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtGui import QPixmap, QPainter, QImage, QMouseEvent
from PyQt5.QtCore import Qt, QMargins, QRectF, QTimer, QSize, QPoint, pyqtSignal

DIR_NAME  = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'image')

DOUNLOAD_COUNT = 100

IMAGE_INTERVAL = 20000

DEFAULT_KEYWORD = '女性ヘアカタログロング'

class MouseEventMixin():
    mouse_left_press = pyqtSignal(QPoint)
    mouse_left_move = pyqtSignal(QPoint)
    mouse_left_release = pyqtSignal(QPoint)
    mouse_left_double_click = pyqtSignal(QMouseEvent)

    def point_to_parent(self, pos):
        return QPoint(self.x() + pos.x(), self.y() + pos.y())

    def mouse_press_event(self, event):
        if (event.button() == Qt.LeftButton):
            pos = self.point_to_parent(event.pos())
            self.mouse_left_press.emit(pos)

    def mouse_move_event(self, event):
        if (event.buttons() & Qt.LeftButton):
            pos = self.point_to_parent(event.pos())
            self.mouse_left_move.emit(pos)

    def mouse_release_event(self, event):
        if (event.button() == Qt.LeftButton):
            pos = self.point_to_parent(event.pos())
            self.mouse_left_release.emit(pos)

    def mouse_double_click_event(self, event):
        if (event.button() == Qt.LeftButton):
            self.mouse_left_double_click.emit(event)

class DownloadWidget(QWidget, MouseEventMixin):
    complete_progress = pyqtSignal()

    def __init__(self, download_keyword, parent = None):
        super(DownloadWidget, self).__init__(parent)
        self.__download_keyword = download_keyword
        self.__progress_bar = None
        self.__downloader = Downloader()
        self.__downloader.progress_download.connect(self.on_progress_download)

        self.init_ui()

    def init_ui(self):
        label = QLabel('カプチーノを入れています．．．', self)
        label.setAlignment(Qt.AlignCenter)

        pbar = QProgressBar(self)
        pbar.setRange(0, DOUNLOAD_COUNT)
        pbar.setTextVisible(False)

        vbox = QVBoxLayout(self)
        vbox.addWidget(label)
        vbox.addWidget(pbar)
        vbox.setContentsMargins(QMargins(16, 16, 16, 16))
        self.setLayout(vbox)

        self.__progress_bar = pbar

    def start_download(self):
        def inner(keyword):
            minsize = (300, 300)
            self.__downloader.download_image(keyword, DOUNLOAD_COUNT, DIR_NAME, minsize)
            self.complete_progress.emit()
        th = threading.Thread(target = inner, args = (self.__download_keyword, ))
        th.start()

    def on_progress_download(self, progress):
        self.__progress_bar.setValue(progress)

    def mousePressEvent(self, event):
        super(DownloadWidget, self).mousePressEvent(event)
        self.mouse_press_event(event)

    def mouseMoveEvent(self, event):
        super(DownloadWidget, self).mouseMoveEvent(event)
        self.mouse_move_event(event)

    def mouseReleaseEvent(self, event):
        super(DownloadWidget, self).mouseReleaseEvent(event)
        self.mouse_release_event(event)

    def mouseDoubleClickEvent(self, event):
        super(DownloadWidget, self).mouseDoubleClickEvent(event)
        self.mouse_double_click_event(event)

class ImageView(QGraphicsView, MouseEventMixin):
    def __init__(self, parent = None):
        super(ImageView, self).__init__(parent)
        self.__image = None
        self.__timer = QTimer(self)
        self.__image_list = None
        self.init_ui()

    def init_ui(self):
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        self.__timer.setInterval(IMAGE_INTERVAL)
        self.__timer.timeout.connect(self.on_timeout)

    def init_image_list(self):
        self.__image_list = [x for x in os.listdir(DIR_NAME) if os.path.isfile(os.path.join(DIR_NAME, x))]

    def start_view(self):
        self.init_image_list()
        self.random_set_image()
        self.__timer.start()

    def set_image(self, filename):
        self.__image = QImage(filename)
        self.setUpdatesEnabled(False)   # ステータスを書き換えないとrepaint()が効かなかった対策．もっとまともな手はないか．．．
        self.setUpdatesEnabled(True)
        self.repaint()

    def random_set_image(self):
        if not self.__image_list:
            return
        image = random.choice(self.__image_list)
        self.__image_list.remove(image)
        self.set_image(os.path.join(DIR_NAME, image))

    def on_timeout(self):
        if not self.__image_list:
            self.init_image_list()
        self.random_set_image()

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
        self.mouse_press_event(event)

    def mouseMoveEvent(self, event):
        super(ImageView, self).mouseMoveEvent(event)
        self.mouse_move_event(event)

    def mouseReleaseEvent(self, event):
        super(ImageView, self).mouseReleaseEvent(event)
        self.mouse_release_event(event)

    def mouseDoubleClickEvent(self, event):
        super(ImageView, self).mouseDoubleClickEvent(event)
        self.mouse_double_click_event(event)

class MainWindow(QWidget):
    def __init__(self, download_keyword, parent = None):
        super(MainWindow, self).__init__(parent, Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.__download_widget = None
        self.__image_view = None
        self.__mouse_left_press_pos = None

        self.init_common_ui()
        if download_keyword:
            self.init_download_ui(download_keyword)
            self.__download_widget.start_download()
        else:
            self.init_image_ui()
            self.__image_view.start_view()

    def init_common_ui(self):
        self.resize(500, 300)
        self.setWindowTitle("cappuccino")

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(vbox)

    def init_download_ui(self, download_keyword):
        self.__download_widget = DownloadWidget(download_keyword)

        layout = self.layout()
        layout.removeWidget(self.__image_view)
        layout.addWidget(self.__download_widget)

        self.__download_widget.mouse_left_press.connect(self.on_mouse_left_press)
        self.__download_widget.mouse_left_move.connect(self.on_mouse_left_move)
        self.__download_widget.mouse_left_release.connect(self.on_mouse_left_release)
        self.__download_widget.mouse_left_double_click.connect(self.on_mouse_left_double_click)
        self.__download_widget.complete_progress.connect(self.on_complete_progress)

    def init_image_ui(self):
        self.__image_view = ImageView(self)

        layout = self.layout()
        layout.removeWidget(self.__download_widget)
        layout.addWidget(self.__image_view)

        self.__image_view.mouse_left_press.connect(self.on_mouse_left_press)
        self.__image_view.mouse_left_move.connect(self.on_mouse_left_move)
        self.__image_view.mouse_left_release.connect(self.on_mouse_left_release)
        self.__image_view.mouse_left_double_click.connect(self.on_mouse_left_double_click)

    def point_to_screen(self, pos):
        return QPoint(self.x() + pos.x(), self.y() + pos.y())

    def on_complete_progress(self):
        self.init_image_ui()
        self.__image_view.start_view()

    def on_mouse_left_press(self, pos):
        self.__mouse_left_press_pos = pos

    def on_mouse_left_move(self, pos):
        if not self.__mouse_left_press_pos:
            return
        screen_pos = self.point_to_screen(pos)
        self.move(QPoint(screen_pos.x() - self.__mouse_left_press_pos.x(), screen_pos.y() - self.__mouse_left_press_pos.y()))

    def on_mouse_left_release(self, pos):
        self.__mouse_left_press_pos = None

    def on_mouse_left_double_click(self, event):
        self.setWindowState(Qt.WindowMinimized)

def main():
    app = QApplication(sys.argv)
    download_keyword = sys.argv[1] if (2 <= len(sys.argv)) else ''
    if not download_keyword and (not os.path.isdir(DIR_NAME) or not [x for x in os.listdir(DIR_NAME) if os.path.isfile(os.path.join(DIR_NAME, x))]):
        download_keyword = DEFAULT_KEYWORD

    window = MainWindow(download_keyword)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
