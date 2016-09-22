import subprocess
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        subprocess.run(['juke', 'add', request.form['song'])

    return render_template('home.html') # add list of musics to template
