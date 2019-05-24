# -*- coding: utf-8 -*-

from flask import Flask, flash, redirect, render_template, request, session, abort
from bokeh.embed import server_document
import subprocess

#this allows the bokeh app running on port 5006 to be accessed by Flask at port 5000
#allow flash to read what is the bokeh server
def bash_command(cmd):
    subprocess.Popen(cmd, shell=True)
bash_command('bokeh serve ./statistics.py --allow-websocket-origin=127.0.0.1:5000')

app = Flask(__name__)

@app.route("/")
def hello():
    script=server_document("http://localhost:5006/statistics1")
    print(script)
    return render_template('hello.html',bokS=script)

if __name__ == "__main__":
    app.run()
    
'''browse the app folder on a terminal and run:
python dynamic.py '''