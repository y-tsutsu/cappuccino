import sys, os, random, threading, argparse, shutil
from downloader import Downloader
from indico import filter_image
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QVBoxLayout, QLabel, QProgressBar, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QImage, QMouseEvent
from PyQt5.QtCore import Qt, QMargins, QRectF, QTimer, QSize, QPoint, pyqtSignal

DOUNLOAD_COUNT = 100

MIN_SIZE = (300, 300)

IMAGE_INTERVAL = 20000

DIR_NAME  = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'image')

DEFAULT_KEYWORD = '女性ヘアカタログロング'

class MouseEventMixin():
    mouse_left_press = pyqtSignal(QPoint)
    mouse_left_move = pyqtSignal(QPoint)
    mouse_left_release = pyqtSignal(QPoint)
    mouse_left_double_click = pyqtSignal(QMouseEvent)

    def mousePressEvent(self, event):
        super(MouseEventMixin, self).mousePressEvent(event)
        if (event.button() == Qt.LeftButton):
            pos = self.mapToGlobal(event.pos())
            self.mouse_left_press.emit(pos)

    def mouseMoveEvent(self, event):
        super(MouseEventMixin, self).mouseMoveEvent(event)
        if (event.buttons() & Qt.LeftButton):
            pos = self.mapToGlobal(event.pos())
            self.mouse_left_move.emit(pos)

    def mouseReleaseEvent(self, event):
        super(MouseEventMixin, self).mouseReleaseEvent(event)
        if (event.button() == Qt.LeftButton):
            pos = self.mapToGlobal(event.pos())
            self.mouse_left_release.emit(pos)

    def mouseDoubleClickEvent(self, event):
        super(MouseEventMixin, self).mouseDoubleClickEvent(event)
        if (event.button() == Qt.LeftButton):
            self.mouse_left_double_click.emit(event)

class DownloadWidget(MouseEventMixin, QWidget):
    complete_progress = pyqtSignal()

    def __init__(self, download_keyword, dirname, is_filter = False, parent = None):
        super(DownloadWidget, self).__init__()
        super(MouseEventMixin, self).__init__(parent)
        self.__download_keyword = download_keyword
        self.__dirname = dirname
        self.__is_filter = is_filter
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
            self.__downloader.download_image(keyword, DOUNLOAD_COUNT, self.__dirname, MIN_SIZE)
            if self.__is_filter:
                filter_image(self.__dirname)
            self.complete_progress.emit()
        th = threading.Thread(target = inner, args = (self.__download_keyword, ))
        th.setDaemon(True)
        th.start()

    def on_progress_download(self, progress):
        self.__progress_bar.setValue(progress)

class ImageView(MouseEventMixin, QGraphicsView):
    def __init__(self, dirname, parent = None):
        super(ImageView, self).__init__()
        super(MouseEventMixin, self).__init__(parent)
        self.__dirname = dirname
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
        self.__image_list = [x for x in os.listdir(self.__dirname) if os.path.isfile(os.path.join(self.__dirname, x))]

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
        self.set_image(os.path.join(self.__dirname, image))

    def on_timeout(self):
        if not self.__image_list:
            self.init_image_list()
        self.random_set_image()

    def paintEvent(self, event):
        super(MouseEventMixin, self).paintEvent(event)

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

class MainWindow(QWidget):
    def __init__(self, download_keyword, dirname, is_filter = False, parent = None):
        super(MainWindow, self).__init__(parent, Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.__dirname = dirname
        self.__download_widget = None
        self.__image_view = None
        self.__mouse_left_press_pos = None

        self.init_common_ui()
        if download_keyword:
            self.init_download_ui(download_keyword, is_filter)
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

    def init_download_ui(self, download_keyword, is_filter):
        self.__download_widget = DownloadWidget(download_keyword, self.__dirname, is_filter, self)

        layout = self.layout()
        layout.removeWidget(self.__image_view)
        layout.addWidget(self.__download_widget)

        self.__download_widget.mouse_left_press.connect(self.on_mouse_left_press)
        self.__download_widget.mouse_left_move.connect(self.on_mouse_left_move)
        self.__download_widget.mouse_left_release.connect(self.on_mouse_left_release)
        self.__download_widget.mouse_left_double_click.connect(self.on_mouse_left_double_click)
        self.__download_widget.complete_progress.connect(self.on_complete_progress)
        self.__download_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__download_widget.customContextMenuRequested.connect(self.on_context_menu_requested)

    def init_image_ui(self):
        self.__image_view = ImageView(self.__dirname, self)

        layout = self.layout()
        layout.removeWidget(self.__download_widget)
        layout.addWidget(self.__image_view)

        self.__image_view.mouse_left_press.connect(self.on_mouse_left_press)
        self.__image_view.mouse_left_move.connect(self.on_mouse_left_move)
        self.__image_view.mouse_left_release.connect(self.on_mouse_left_release)
        self.__image_view.mouse_left_double_click.connect(self.on_mouse_left_double_click)
        self.__image_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__image_view.customContextMenuRequested.connect(self.on_context_menu_requested)

    def on_complete_progress(self):
        self.init_image_ui()
        self.__image_view.start_view()

    def on_mouse_left_press(self, gpos):
        self.__mouse_left_press_pos = self.mapTo(self, self.mapFromGlobal(gpos))

    def on_mouse_left_move(self, gpos):
        if not self.__mouse_left_press_pos:
            return
        self.move(gpos - self.__mouse_left_press_pos)

    def on_mouse_left_release(self, gpos):
        self.__mouse_left_press_pos = None

    def on_mouse_left_double_click(self, event):
        self.setWindowState(Qt.WindowMinimized)

    def on_context_menu_requested(self, pos):
        def inner_clear():
            result = QMessageBox.question(self, self.windowTitle(), 'Delete all image ?', QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if result == QMessageBox.Ok:
                shutil.rmtree(self.__dirname)

        menu = QMenu(self)
        hide = QAction('Hide', self)
        hide.triggered.connect(lambda: self.setWindowState(Qt.WindowMinimized))
        clear = QAction('Clear', self)
        clear.triggered.connect(inner_clear)
        exit = QAction('Exit', self)
        exit.triggered.connect(lambda: self.close())
        menu.addAction(hide)
        menu.addAction(clear)
        menu.addAction(exit)
        menu.exec(self.mapToGlobal(pos))

def main():
    parser = argparse.ArgumentParser(description = 'cappuccino')
    parser.add_argument('download_keyword', nargs = '?', default = '', help = 'Download Keyword')
    parser.add_argument('-f', '--filter', action = 'store_true', help = 'Content Filtering')
    args = parser.parse_args()

    download_keyword = args.download_keyword
    if not download_keyword and (not os.path.isdir(DIR_NAME) or not [x for x in os.listdir(DIR_NAME) if os.path.isfile(os.path.join(DIR_NAME, x))]):
        download_keyword = DEFAULT_KEYWORD

    app = QApplication(sys.argv)
    window = MainWindow(download_keyword, DIR_NAME, args.filter)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
