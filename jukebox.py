import threading, os, time, sys, youtube_dl
from queue import Queue
from pytube import YouTube

#remove o fifo anterior se exisitir
def rmOldFifo():
    try:
        os.remove(pipe_name)
    except OSError:
        pass

# Faz o download do URL e devolve o nome do ficheiro
def download( record_url ):
    yt = YouTube(record_url)
    fname = yt.filename
    ydl_opts = {
        'outtmpl': 'records/' + fname + '.mp3',
        'format': 'bestaudio/best',
        'verbose': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([record_url])
    return fname

# Fica a ler do fifo o URL das musicas 
# e coloca-o na queue,e começa o download
def readFromFifo():
    while True:
        request = pipein.readline()
        if request.split(' ', 1)[0] == 'add':
           record = request.split(' ', 1)[1]
           record_name = download(record)
           q.put(record_name)
        elif request.split(' ', 1)[0] == 'list':
             print(q)

# Lê da queue e toca as musicas
def playList():
    while True:
        record_name = q.get()
        if os.fork() == 0:
            os.execlp('mpv', 'mpv', 'records/' + record_name + '.mp3')
            os._exit(1)
        else:
            os.wait()
            q.task_done()

q = Queue()
pipe_name = 'records_holder'
os.makedirs( 'records', 666, True)
rmOldFifo()
os.mkfifo(pipe_name)
pipein = open(pipe_name, 'r')
reader = threading.Thread(target = readFromFifo)
reader.daemon = True
reader.start()
#player = threading.Thread(target = playList) 
#player.daemon = True
#player.start()

#readFromFifo()
playList()
