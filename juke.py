import os, sys

pipe_name = 'records_holder'
pipeout = os.open(pipe_name, os.O_WRONLY)
if sys.argv[1].lower() == 'add':
    msg = 'add ' + sys.argv[2]
    os.write(pipeout, msg.encode() )
elif sys.argv[1].lower() == 'list':
    os.write(pipeout, 'list')
