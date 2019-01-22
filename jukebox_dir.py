import os
import sys
import logging
import configparser
import itertools
import shutil
import time

mpv = lambda file: os.system("/usr/bin/mpv {} --no-video".format(file))
mpg123 = lambda file: os.system("/usr/bin/mpg123 {}".format(file))

def music_queue(path):
    while 1:
        files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

        if files:
            yield min(files, key=lambda f: os.path.getctime(f))
        else:
            break

def read_properties_file(filepath):
    """
    http://stackoverflow.com/a/26859985
    """
    parser = configparser.ConfigParser()
    with open(filepath) as lines:
        lines = itertools.chain(("[top]",), lines)  # This line does the trick.
        parser.read_file(lines)

    return dict(parser.items('top'))

def play_file(path):
    props = read_properties_file(path)

    if 'mp3' in props:
        f = props['mp3']
        mpg123(f)

    elif 'file' in props:
        f = props['file']
        mpv(f)

    elif 'youtube' in props:
        yt_link = props['youtube']
        mpv(yt_link)

def play_dir(path):
    for music in music_queue(path):
        play_file(music)
        os.remove(music)

def main():
    while 1:
        play_dir(sys.argv[1])
        time.sleep(10)

if __name__ == "__main__":
    main()
