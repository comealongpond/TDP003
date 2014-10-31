# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import abort
import data

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    db = data.load('data.json')
    project_list = data.search(db, sort_by='start_date')
    return render_template("index.html", title = 'Hem', project = project_list[0])
@app.route('/techniques')
def render_techniques():
    db = data.load('data.json')
    technique_dict = data.get_technique_stats(db)
    return render_template("techniques.html", title = "Tekniker", techniques = technique_dict, projects = data.search(db))
    
def search(fields):
    db = data.load('data.json')
    return data.search(db, search=str(fields) ,search_fields = ['project_no'])[0]

def search_all(sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None):
    db = data.load('data.json')
    return data.search(db, sort_by, sort_order, techniques, search, search_fields)

@app.route('/project/<pid>')
def show_project(pid):
    try:
        db = data.load('data.json')
        project_var = data.search(db, search=str(pid), search_fields=['project_no'])
        print(project_var)
        return render_template("project.html", title="project <pid>", projectid = pid, project = project_var)
    except:
        abort(404) #give error 404

@app.route('/list', methods = ['GET', 'POST'])
def search_page():
    db = data.load('data.json')
    technique_dict = data.get_technique_stats(db)
    if request.method == 'POST':
        if request.form['search-text'] == '':
            text = None
        else:
            text = request.form['search-text']
        if request.form.getlist('techniques') == []:
            technique = None
        else:
            technique = request.form.getlist('techniques')
        if request.form.getlist('fields') == []:
            search_fields = None
        else:
            search_fields = request.form.getlist('fields')
        return render_template("search.html", title = "search", techniques = technique_dict , sort=request.form['sort_by'], search_text = text, order = request.form['sort_order'] , tech = technique, search_field = search_fields, header = 'Search Results')
    else:
        return render_template("search.html", title = "search", techniques = technique_dict , sort='start_date' , search_text = None, order = 'desc' , tech = None, search_field = None, header = 'All Projects')

app.jinja_env.globals.update(search=search)
app.jinja_env.globals.update(search_all=search_all)

if __name__ == "__main__":
    app.run(debug = True)
