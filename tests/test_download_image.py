import unittest
from os import mkdir
from pathlib import Path
from shutil import rmtree

from cv2 import imread

from downloader import Downloader


class TestDownloadImage(unittest.TestCase):
    TEST_DIR_NAME = 'test_image'

    def setUp(self):
        mkdir(TestDownloadImage.TEST_DIR_NAME)

    def tearDown(self):
        rmtree(TestDownloadImage.TEST_DIR_NAME)

    def test_download_image(self):
        FILE_COUNT = 10
        MIN_WIDTH = 400
        MIN_HEIGHT = 300

        d = Downloader()
        d.download_images('ネコ', TestDownloadImage.TEST_DIR_NAME, FILE_COUNT, (MIN_WIDTH, MIN_HEIGHT))

        files = [x for x in Path(TestDownloadImage.TEST_DIR_NAME).glob('*') if x.is_file()]
        self.assertEqual(FILE_COUNT, len(files))

        for f in files:
            img = imread(str(f))
            self.assertIsNotNone(img)
            h, w, _ = img.shape
            self.assertGreaterEqual(w, MIN_WIDTH)
            self.assertGreaterEqual(h, MIN_HEIGHT)

    def test_download_image_default(self):
        d = Downloader()
        d.download_images('ネコ', TestDownloadImage.TEST_DIR_NAME)

        files = [x for x in Path(TestDownloadImage.TEST_DIR_NAME).glob('*') if x.is_file()]
        self.assertEqual(100, len(files))

        for f in files:
            img = imread(str(f))
            self.assertIsNotNone(img)


if __name__ == '__main__':
    unittest.main()
