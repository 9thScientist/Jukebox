import subprocess
from os.path import isfile
import os.path
from os import listdir
from flask import Flask, render_template
app = Flask(__name__)

dir = os.path.expanduser('~/Queue/')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        attrib = "youtube={}".format(request.form['song'])
        
        with open(request.form['song']) as f:
            f.write(attrib)

    return render_template('home.html') # TODO: add list of musics to template
