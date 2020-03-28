import json
import shutil
from os import mkdir, path, remove
from time import sleep

from requests import get

from bs4 import BeautifulSoup
from cv2 import imread


class Downloader:
    def __init__(self, progress_callback=None):
        self.__progress_callback = progress_callback
        self.__headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.107 Safari/537.36'}

    def download_images(self, keyword, dirname, download_num=100, minsize=(0, 0)):
        if path.isdir(dirname):
            shutil.rmtree(dirname)
            sleep(1)
        mkdir(dirname)

        count = self.__crawring(keyword, dirname, download_num, minsize)
        print(f'{count} files downloaded.')

    def __crawring(self, keyword, dirname, download_num, minsize):
        extensions = ['.jpg', '.jpeg', '.gif', '.png']
        downloaded_urls = []
        success_urls = []
        for i in range(50):
            url = f'https://www.bing.com/images/async?q={keyword}&first={i * 20}'
            print(f'search url: {url}')
            html = self.__get_html_string(url)
            if not html:
                print('html is empty!!')
                continue
            image_urls = self.__get_urls(html, extensions, downloaded_urls)
            count = self.__get_resource(image_urls, success_urls, dirname, download_num, minsize)
            if download_num <= count:
                break
        return count

    def __get_html_string(self, url):
        try:
            response = get(url, headers=self.__headers)
            return response.content.decode('utf-8')
        except Exception as ex:
            print(ex)
            return ''

    def __get_urls(self, html, extensions, downloaded_urls):
        result = []
        soup = BeautifulSoup(html, 'html.parser')
        for a_tag in soup.find_all('a', {'class': 'iusc'}):
            j = json.loads(a_tag.attrs['m'])
            murl = j['murl']
            _, ext = path.splitext(murl)
            if ext in extensions and murl not in downloaded_urls:
                downloaded_urls.append(murl)
                result.append(murl)
        return result

    def __get_resource(self, image_urls, success_urls, dirname, download_num, minsize):
        count = len(success_urls)
        for url in image_urls:
            try:
                _, ext = path.splitext(url)
                savename = path.join(dirname, f'{count:03}{ext}')
                print(f'download ---> [{path.basename(savename)}]')
                response = get(url, headers=self.__headers)
                with open(savename, 'wb') as f:
                    f.write(response.content)
                result, (w, h) = self.__check_size(savename, minsize)
                if result:
                    count += 1
                    success_urls.append(url)
                    if self.__progress_callback:
                        self.__progress_callback(count)
                else:
                    print(f'image too small ... [{path.basename(savename)}] : ({w}, {h})')
                    remove(savename)
                if download_num <= count:
                    break
            except Exception as ex:
                print(ex)
                print(f'download failed ... [{path.basename(savename)}]')
        return count

    def __check_size(self, filename, minsize):
        img = imread(filename)
        height, width, _ = img.shape
        result = True if minsize[0] <= width and minsize[1] <= height else False
        return (result, (width, height))
