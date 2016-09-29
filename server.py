import subprocess
from flask import request, Flask, render_template
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        subprocess.run(['./juke.py', 'add', request.form['song']])

    return render_template('home.html') # add list of musics to template

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
