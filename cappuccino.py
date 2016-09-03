from downloader import download_image

def main():
    keyword = 'ご注文はうさぎですか？？'
    dirname  = 'image'
    minsize = (400, 400)
    download_image(keyword, 100, dirname, minsize)

if __name__ == '__main__':
    main()
