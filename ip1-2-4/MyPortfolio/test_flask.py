# -*- coding: utf-8 -*-
from flask import Flask, render_template
import data

app = Flask(__name__)
db = data.load('data.json')

@app.route('/')
def index():
    project_list = data.search(db, sort_by='start_date')
    return render_template("index.html", title = 'Hem', project = project_list[0])
@app.route('/techniques')
def render_techniques():
    technique_dict = data.get_technique_stats(db)
    project_list = data.search(db)
    return render_template("techniques.html", title = "Tekniker", techniques = technique_dict, project = project_list)
    

if __name__ == "__main__":
    app.run(debug = True)
