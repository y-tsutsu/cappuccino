# cappuccino

Simple image viewer with download

# Requirements

* beautifulsoup4
* OpenCV
* PySide6

# Initialize (Pipenv)

```console
$ pip install pipenv
$ pipenv sync --dev
```

# How to

## Download image and Display

```console
$ pipenv run python cappuccino.py download_keyword
```

```console
usage: cappuccino.py [-h] [download_keyword]

cappuccino

positional arguments:
  download_keyword  image keyword to download

optional arguments:
  -h, --help        show this help message and exit
```

## Display of the downloaded image

```console
$ pipenv run start
or
$ pipenv run python cappuccino.py
```

# Build

## by PyInstaller

```console
$ pipenv run build-pyins
or
$ pipenv run pyinstaller cappuccino.py --onefile --noconsole --clean --icon=cappuccino.ico --add-data ./cappuccino.ico;. --add-data ./qml/*;./qml/.
```

## by Nuitka

```console
$ pipenv run build-nuitka
or
$ python -m nuitka --standalone --onefile --windows-console-mode=disable --windows-icon-from-ico=cappuccino.ico --enable-plugin=pyside6 --include-qt-plugins=qml --include-data-dir=qml=qml --include-data-files=cappuccino.ico=cappuccino.ico cappuccino.py
```
