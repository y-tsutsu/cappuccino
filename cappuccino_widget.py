import random
import shutil
import sys
from argparse import ArgumentParser
from os import path
from pathlib import Path
from threading import Thread

from PySide2 import __version__ as PySideVer
from PySide2.QtCore import QMargins, QPoint, QRectF, Qt, QTimer, Signal
from PySide2.QtCore import __version__ as QtVer
from PySide2.QtGui import QIcon, QImage, QMouseEvent, QPainter
from PySide2.QtWidgets import (QAction, QApplication, QDesktopWidget,
                               QGraphicsView, QLabel, QMenu, QMessageBox,
                               QProgressBar, QVBoxLayout, QWidget)

from downloader import Downloader

DOUNLOAD_COUNT = 100

MIN_SIZE = (300, 300)

IMAGE_INTERVAL = 20000

IMAGES_DIR_NAME = path.join(path.abspath(path.dirname(sys.argv[0])), 'images')

DEFAULT_KEYWORD = '女性ヘアカタログロング'


class MouseEventMixin:
    mouse_left_press = Signal(QPoint)
    mouse_left_move = Signal(QPoint)
    mouse_left_release = Signal(QPoint)
    mouse_left_double_click = Signal(QMouseEvent)

    def __init__(self):
        pass

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
    __progress_download = Signal(int)
    complete_download = Signal()

    def __init__(self, download_keyword, dirname, parent=None):
        super(DownloadWidget, self).__init__()
        super(MouseEventMixin, self).__init__(parent)
        self.__download_keyword = download_keyword
        self.__dirname = dirname
        self.__progress_bar = None
        self.__downloader = Downloader(self.progress_download_callback)
        self.__progress_download.connect(self.on_progress_download)

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
        def _inner(keyword, dirname):
            self.__downloader.download_images(keyword, dirname, DOUNLOAD_COUNT, MIN_SIZE)
            self.complete_download.emit()
        th = Thread(target=_inner, args=(self.__download_keyword, self.__dirname))
        th.setDaemon(True)
        th.start()

    def progress_download_callback(self, progress):
        self.__progress_download.emit(progress)

    def on_progress_download(self, progress):
        self.__progress_bar.setValue(progress)


class ImageView(MouseEventMixin, QGraphicsView):
    def __init__(self, dirname, parent=None):
        super(ImageView, self).__init__()
        super(MouseEventMixin, self).__init__(parent)
        self.__dirname = dirname
        self.__image = None
        self.__image_list = []
        self.__timer = QTimer(self)
        self.init_ui()

    def init_ui(self):
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        self.__timer.setInterval(IMAGE_INTERVAL)
        self.__timer.timeout.connect(self.on_timeout)

    def init_image_list(self):
        self.__image_list = [str(x) for x in Path(self.__dirname).iterdir() if x.is_file()]

    def start_view(self):
        self.init_image_list()
        self.random_set_image()
        self.__timer.start()

    def set_image(self, filename):
        self.setUpdatesEnabled(False)
        self.__image = QImage(filename)
        self.repaint()
        self.setUpdatesEnabled(True)

    def random_set_image(self):
        if not self.__image_list:
            return
        image = random.choice(self.__image_list)
        self.__image_list.remove(image)
        self.set_image(path.join(self.__dirname, image))

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
    def __init__(self, download_keyword, dirname, parent=None):
        super(MainWindow, self).__init__(parent, Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.__dirname = dirname
        self.__download_widget = None
        self.__image_view = None
        self.__mouse_left_press_pos = None
        self.__menu = QMenu(self)

        self.init_common_ui()
        if download_keyword:
            self.init_download_ui(download_keyword)
            self.__download_widget.start_download()
        else:
            self.init_image_ui()
            self.__image_view.start_view()

    def init_common_ui(self):
        height = QDesktopWidget().height() // 5
        self.resize(height * 5 // 3, height)
        self.setWindowTitle('cappuccino')

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(vbox)

        self.init_menu()

    def init_menu(self):
        def _inner_clear():
            result = QMessageBox.question(self, self.windowTitle(), 'Delete all images ?',
                                          QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if result == QMessageBox.Ok:
                shutil.rmtree(self.__dirname)

        _window = self

        def _inner_toggle(state):
            if state:
                _window.setWindowFlags(_window.windowFlags() | Qt.WindowStaysOnTopHint)
            else:
                _window.setWindowFlags(_window.windowFlags() & ~Qt.WindowStaysOnTopHint)
            _window.show()

        top = QAction('&Top', self, checkable=True)
        top.triggered.connect(_inner_toggle)
        top.setChecked(True)
        hide = QAction('&Hide', self)
        hide.triggered.connect(lambda: self.setWindowState(Qt.WindowMinimized))
        clear = QAction('&Clear', self)
        clear.triggered.connect(_inner_clear)
        exit_ = QAction('&Exit', self)
        exit_.triggered.connect(lambda: self.close())
        self.__menu.addAction(top)
        self.__menu.addAction(hide)
        self.__menu.addAction(clear)
        self.__menu.addAction(exit_)

    def init_download_ui(self, download_keyword):
        self.__download_widget = DownloadWidget(download_keyword, self.__dirname, self)

        layout = self.layout()
        layout.removeWidget(self.__image_view)
        layout.addWidget(self.__download_widget)

        self.__download_widget.mouse_left_press.connect(self.on_mouse_left_press)
        self.__download_widget.mouse_left_move.connect(self.on_mouse_left_move)
        self.__download_widget.mouse_left_release.connect(self.on_mouse_left_release)
        self.__download_widget.mouse_left_double_click.connect(self.on_mouse_left_double_click)
        self.__download_widget.complete_download.connect(self.on_complete_download)
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

    def on_complete_download(self):
        self.init_image_ui()
        self.__image_view.start_view()

    def on_mouse_left_press(self, gpos):
        self.__mouse_left_press_pos = self.mapFromGlobal(gpos) - self.mapFromGlobal(self.pos())

    def on_mouse_left_move(self, gpos):
        if not self.__mouse_left_press_pos:
            return
        self.move(gpos - self.__mouse_left_press_pos)

    def on_mouse_left_release(self, gpos):
        self.__mouse_left_press_pos = None

    def on_mouse_left_double_click(self, event):
        self.setWindowState(Qt.WindowMinimized)

    def on_context_menu_requested(self, pos):
        self.__menu.exec_(self.mapToGlobal(pos))


def exist_images():
    return path.isdir(IMAGES_DIR_NAME) and any([x.is_file() for x in Path(IMAGES_DIR_NAME).iterdir()])


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relative)
    return path.join(relative)


def main():
    print(f'PySide2=={PySideVer} Qt=={QtVer}')

    parser = ArgumentParser(description='cappuccino')
    parser.add_argument('download_keyword', nargs='?', default='', help='image keyword to download')
    args = parser.parse_args()

    download_keyword = args.download_keyword
    if not download_keyword and not exist_images():
        download_keyword = DEFAULT_KEYWORD

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('cappuccino.ico')))
    window = MainWindow(download_keyword, IMAGES_DIR_NAME)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
