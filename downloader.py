import os, sys, shutil, time
import bs4, urllib.request
from PIL import Image

def download_image(keyword, download_num, dirname, minsize):
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
        time.sleep(1)
    os.mkdir(dirname)

    extensions = ['.jpg', '.jpeg', '.gif', '.png']
    count = 0
    num = 0
    ONE_PAGE_NUM = 20
    while num < download_num:
        count += 1
        url = 'http://image.search.yahoo.co.jp/search?p={0}&ktot=30&dtot=0&ei=UTF-8&xargs={1}&b={2}'.format(urllib.request.quote(keyword), count, ONE_PAGE_NUM * count + 1)
        num += crawring(url, extensions, dirname, download_num - num, minsize)
        if download_num * 2 < count * ONE_PAGE_NUM:
            break

def crawring(url, extensions, dirname, download_num, minsize):
    # 指定したURLのHTMLを取得
    html = get_html_string(url)
    if len(html) < 1:
        print('damepo!!')
        sys.exit(1)

    # リソース取得
    return get_resource(html, extensions, dirname, download_num, minsize)

def get_html_string(url):
    decoded_html = ''

    # HTMLを取得
    try:
        request = urllib.request.urlopen(url)
        html = request.read()
    except:
        return decoded_html

    # HTMLをデコード
    decoded_html = html.decode('utf_8')

    return decoded_html

def get_resource(html, extensions, dirname, download_num, minsize):
    resource_list = []

    soup = bs4.BeautifulSoup(html)
    for a_tag in soup.find_all('a'):
        href_str = a_tag.get('href')
        try:
            (path, ext) = os.path.splitext(href_str)
            if ext in extensions:
                resource_list.append(href_str)
        except:
            pass

    resource_list = sorted(set(resource_list), key = resource_list.index)
    count = 0
    for resource in resource_list:
        try:
            filename = os.path.basename(resource)
            savename = '{0}\\{1}'.format(dirname, filename)
            if os.path.exists(savename):
                continue
            print('download ---> [{0}]'.format(filename))
            request = urllib.request.urlopen(resource)
            with open(savename, 'wb') as f:
                f.write(request.read())
            if check_size(savename, minsize):
                count += 1
            else:
                os.remove(savename)
            if download_num <= count:
                break
        except Exception as e:
            print(e)
            print('download failed ... [{0}]'.format(filename))

    return count

def check_size(filename, minsize):
    f = Image.open(filename)
    return True if minsize[0] <= f.size[0] and minsize[1] <= f.size[1] else False
