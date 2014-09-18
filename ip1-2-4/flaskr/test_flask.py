# -*- coding: utf-8 -*-
from flask import Flask, render_template
import uppgift1

app = Flask(__name__)

@app.route('/')
def index():
    personlist = uppgift1.format_by('name', uppgift1.personlist)
    user = { 'nickname': 'Miguel' } # fake user
    return render_template("index.html",title = 'Home',user = user, personlist = personlist)
@app.route('/hello')
def hello():
    return 'Hej'
    

if __name__ == "__main__":
    app.run()
