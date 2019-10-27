# cappuccino

Simple image viewer with download

# Requirements

* beautifulsoup4
* OpenCV
* PyQt5
* Selenium

# Initialize (Pipenv)

```console
$ pip install pipenv
$ pipenv sync --dev
```

# How to

## Download image and Display (by selenium)

```console
$ pipenv run python cappuccino.py [-s] download_keyword
```

```console
usage: cappuccino.py [-h] [-s] [download_keyword]

cappuccino

positional arguments:
  download_keyword  image keyword to download

optional arguments:
  -h, --help        show this help message and exit
  -s, --selenium    download by selenium
```

### Selenium (Chrome)

Save ChromeDriver to current directory  
[https://sites.google.com/a/chromium.org/chromedriver/home](https://sites.google.com/a/chromium.org/chromedriver/home)

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
$ pipenv run pyinstaller cappuccino.py --onefile --noconsole --clean
```
