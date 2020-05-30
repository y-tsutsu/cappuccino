# cappuccino

Simple image viewer with download

# Requirements

* beautifulsoup4
* OpenCV
* PyQt5

# Initialize (Pipenv)

```console
$ pip install pipenv
$ pipenv sync --dev
```

# How to

## Download image and Display (by selenium)

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

# Build by Pyinstaller

```console
$ pipenv run build
or
$ pipenv run pyinstaller cappuccino.py --onefile --noconsole --clean --icon=cappuccino.ico
```
