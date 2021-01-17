import shutil
import sys
from argparse import ArgumentParser
from os import path
from pathlib import Path
from threading import Thread

from PySide2 import __version__ as PySideVer
from PySide2.QtCore import (Property, QCoreApplication, QObject, Qt, Signal,
                            Slot)
from PySide2.QtCore import __version__ as QtVer
from PySide2.QtGui import QGuiApplication, QIcon
from PySide2.QtQml import QQmlApplicationEngine

from downloader import Downloader

DOUNLOAD_COUNT = 100

MIN_SIZE = (300, 300)

IMAGE_INTERVAL = 20000

IMAGES_DIR_NAME = path.join(path.abspath(path.dirname(sys.argv[0])), 'images')

DEFAULT_KEYWORD = '女性ヘアカタログロング'


class MainModel(QObject):
    is_download_changed = Signal(bool)

    def __init__(self, is_download, dirname, parent=None):
        super().__init__(parent)
        self.__is_download = is_download
        self.__dirname = dirname

    @Property(bool, notify=is_download_changed)
    def is_download(self):
        return self.__is_download

    @is_download.setter
    def is_download(self, value):
        if self.__is_download != value:
            self.__is_download = value
            self.is_download_changed.emit(self.__is_download)

    @Slot()
    def clear(self):
        shutil.rmtree(self.__dirname)

    def on_complete_download(self):
        self.is_download = False


class DownloaderModel(QObject):
    prog_value_changed = Signal(int)
    prog_max_changed = Signal(int)
    complete_download = Signal()

    def __init__(self, download_keyword, dirname, parent=None):
        super().__init__(parent)
        self.__prog_value = 0
        self.__download_keyword = download_keyword
        self.__dirname = dirname
        self.__downloader = Downloader(self.progress_download_callback)

    @Property(int, notify=prog_value_changed)
    def prog_value(self):
        return self.__prog_value

    @prog_value.setter
    def prog_value(self, value):
        if self.__prog_value != value:
            self.__prog_value = value
            self.prog_value_changed.emit(self.__prog_value)

    @Property(int, notify=prog_max_changed)
    def prog_max(self):
        return DOUNLOAD_COUNT

    @Slot()
    def start_download(self):
        def _inner(keyword, dirname):
            self.__downloader.download_images(keyword, dirname, DOUNLOAD_COUNT, MIN_SIZE)
            self.complete_download.emit()
        th = Thread(target=_inner, args=(self.__download_keyword, self.__dirname))
        th.setDaemon(True)
        th.start()

    def progress_download_callback(self, progress):
        self.prog_value = progress


def exist_images():
    return path.isdir(IMAGES_DIR_NAME) and any([x.is_file() for x in Path(IMAGES_DIR_NAME).iterdir()])


def initialize_qt():
    sys.argv += ['--style', 'material']

    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QCoreApplication.setAttribute(Qt.AA_UseOpenGLES)


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

    initialize_qt()

    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('cappuccino.ico')))

    is_download = download_keyword != ''
    mmodel = MainModel(is_download, IMAGES_DIR_NAME)
    dmodel = DownloaderModel(download_keyword, IMAGES_DIR_NAME)
    dmodel.complete_download.connect(mmodel.on_complete_download)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('mmodel', mmodel)
    engine.rootContext().setContextProperty('dmodel', dmodel)
    engine.load(path.join(path.abspath(path.dirname(sys.argv[0])), resource_path('qml/Main.qml')))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
