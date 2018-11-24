# cappuccino

Simple image viewer

# Requirements

* beautifulsoup4
* IndicoIo
* Pillow
* PyQt5
* Selenium

# How to

Download image and Display (filter mature content) (by Selenium)
```console
$ python cappuccino.py image_keyword [-f] [-s]
```

Selenium(Chrome)  
[https://sites.google.com/a/chromium.org/chromedriver/home](https://sites.google.com/a/chromium.org/chromedriver/home)

Display of the downloaded image
```console
$ python cappuccino.py
```

# Pipenv

```console
$ pip install pipenv
$ pipenv install --dev
$ pipenv run start
```

# Pyinstaller

```console
$ pip install pyinstaller
$ pyinstaller cappuccino.py --onefile --noconsole --clean
```
