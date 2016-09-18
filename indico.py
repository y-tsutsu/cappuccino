import os, shutil, indicoio

indicoio.config.api_key = 'b6fb24c9b507d984c8c9cf91c01e910d'

def filter_image(dirname):
    file = [y for y in [os.path.join(dirname, x) for x in os.listdir(dirname)] if os.path.isfile(y)]
    value = indicoio.content_filtering(file)
    filter_file = [x[0] for x in zip(file, value) if 0.5 < x[1]]
    filter_dir = os.path.join(dirname, 'filter')
    if filter_file and not os.path.exists(filter_dir):
        os.mkdir(filter_dir)
    for x in filter_file:
        shutil.move(x, filter_dir)
