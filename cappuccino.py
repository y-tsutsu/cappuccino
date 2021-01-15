import sys
from os import path

from PySide2 import __version__ as PySideVer
from PySide2.QtCore import QCoreApplication, Qt
from PySide2.QtCore import __version__ as QtVer
from PySide2.QtGui import QGuiApplication, QIcon
from PySide2.QtQml import QQmlApplicationEngine


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relative)
    return path.join(relative)


def main():
    sys.argv += ['--style', 'material']

    print(f'PySide2=={PySideVer} Qt=={QtVer}')

    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QCoreApplication.setAttribute(Qt.AA_UseOpenGLES)

    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('cappuccino.ico')))

    engine = QQmlApplicationEngine()
    engine.load(path.join(path.dirname(sys.argv[0]), resource_path('qml/main.qml')))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
