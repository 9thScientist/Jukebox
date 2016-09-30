import subprocess
import os.path
import string
import random

from flask import request, Flask, render_template

dir = os.path.expanduser('/home/alarm/Queue/')
app = Flask(__name__)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        attrib = "youtube={}".format(request.form['song'])
        filename = os.path.join(dir, id_generator())
        
        with open(filename, 'w') as f:
            f.write(attrib)

    return render_template('home.html') # TODO: add list of musics to template

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
