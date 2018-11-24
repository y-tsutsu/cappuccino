import json
import os
import shutil
import sys
import time
import urllib.request

import bs4
from PIL import Image
from PyQt5.QtCore import QObject, pyqtSignal
from selenium import webdriver


class Downloader(QObject):
    progress_download = pyqtSignal(int)

    def download_image(self, keyword, download_num, dirname, minsize, is_selenium):
        if os.path.isdir(dirname):
            shutil.rmtree(dirname)
            time.sleep(1)
        os.mkdir(dirname)

        extensions = ['jpg', 'jpeg', 'gif', 'png']
        url = 'https://www.google.com/search?q={}&hl=ja&source=lnms&tbm=isch'.format(
            urllib.request.quote(keyword))
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.113 Safari/537.36 Viv/2.1.1337.51'}

        count = self.__crawring(url, header, extensions,
                                dirname, download_num, minsize, is_selenium)
        print('{} files downloaded.'.format(count))

    def __crawring(self, url, header, extensions, dirname, download_num, minsize, is_selenium):
        # 指定したURLのHTMLを取得
        html = self.__get_html_string(url, header, is_selenium)
        if html == '':
            print('damepo!!')
            sys.exit(1)

        # リソース取得
        return self.__get_resource(html, extensions, dirname, download_num, minsize)

    def __get_html_string(self, url, header, is_selenium):
        html = ''

        # HTMLを取得
        driver = None
        try:
            if is_selenium:
                driver = webdriver.Chrome()
                driver.minimize_window()
                for i in range(3):
                    driver.get(url)
                    driver.execute_script(
                        'window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(1)
                time.sleep(1)
                html = driver.page_source
            else:
                request = urllib.request.urlopen(
                    urllib.request.Request(url, headers=header))
                html = request.read().decode('utf_8')
        except Exception as ex:
            print(ex)
        finally:
            if driver:
                driver.close()
                pass

        return html

    def __get_resource(self, html, extensions, dirname, download_num, minsize):
        resource_list = []

        soup = bs4.BeautifulSoup(html)
        for div_tag in soup.find_all('div', {'class': 'rg_meta'}):
            j = json.loads(div_tag.text)
            if j['ity'] in extensions:
                resource_list.append(j['ou'])

        count = 0
        for resource in resource_list:
            try:
                filename = os.path.basename(resource)
                if '?' in filename:
                    filename = filename[:filename.index('?')]
                savename = os.path.join(dirname, filename)
                if os.path.isfile(savename):
                    continue
                print('download ---> [{0}]'.format(filename))
                request = urllib.request.urlopen(resource)
                with open(savename, 'wb') as f:
                    f.write(request.read())
                if self.__check_size(savename, minsize):
                    count += 1
                    self.progress_download.emit(count)
                else:
                    os.remove(savename)
                if download_num <= count:
                    break
            except Exception as e:
                print(e)
                print('download failed ... [{0}]'.format(filename))

        return count

    def __check_size(self, filename, minsize):
        f = Image.open(filename)
        return True if minsize[0] <= f.size[0] and minsize[1] <= f.size[1] else False
