import os
import sys
import logging
import configparser
import itertools
import shutil

logger = logging.getLogger(__name__)
level = logging.DEBUG
# level = logging.INFO
try:
    import coloredlogs
    coloredlogs.install(level=level)
except ImportError:
    logging.basicConfig(level=level)
    logger.info("Not using coloredlogs, because coloredlogs is not installed.")

try:
    CACHE = get_cache()
except:
    e = sys.exc_info()[0]
    logger.warning(e)
    CACHE = None


def read_properties_file(filepath):
    """
    http://stackoverflow.com/a/26859985
    """
    parser = configparser.ConfigParser()
    with open(filepath) as lines:
        lines = itertools.chain(("[top]",), lines)  # This line does the trick.
        parser.read_file(lines)

    return dict(parser.items('top'))

# def get_cache():
#     home_cache = os.environ['XDG_CACHE_HOME']
#     cache = os.path.join(home_cache, 'jukebox')

#     if os.isdir(cache):
#         logger.debug("Cache exists.")
#     elif os.i.sfile(cache):
#         logger.warning("Cache is a file! Remove this file to enable cache.")
#         return None
#     else: # doesn't exist
#         logger.debug("Cache doesn't exists. Creating it...")
#         os.mkdir(cache)
#         logger.debug("Cache created.")

#     return cache

def next_music(files):

    def sortkey(pathfile):
        n = ""
        for char in os.path.basename(pathfile):
            if not(char.isdigit()):
                break
            n += char

        return int(n)

    # logger.debug("Excluding these files: {}".format(
    #     [f for f in files if not(os.path.basename(f)[0].isdigit())]))
    
    return min([f for f in files if os.path.basename(f)[0].isdigit()], key=sortkey)


def play_dir(path):
    while 1:
        files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        logger.debug("Found {} files in path".format(len(files)))
        
        try:
            next = next_music(files)
        except ValueError:
            logger.debug("No musics on queue. Exiting")
            break

        logger.debug("Playing from file {}".format(next))
        play_file(next)
        logger.debug("Removed {}".format(next))
        os.remove(next)

mpv = lambda file: os.system("/usr/bin/mpv {}".format(file))

def play_file(path):

    props = read_properties_file(path)

    if 'cache' in props:
        file = props['cache']
    elif 'file' in props:
        file = props['file']
    elif 'youtube' in props:
        file = props['youtube']

    mpv(file)


def main():
    play_dir(sys.argv[1])

if __name__ == "__main__":
    main()
