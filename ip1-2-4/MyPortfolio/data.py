"""This module contains all functions needed for project website"""

import json
import logging
import logging.config
import os.path
import operator

def log_call(message, type_of = 'info'):
    """Logs message into a logfile
    Usage: log_call(message)"""
    type_of_list = {'info' : logging.info, 'warning' : logging.warning}
    logging.basicConfig(filename = 'datalog.log', level = logging.INFO , format='%(asctime)s %(levelname)s %(message)s')
    type_of_list[type_of](message)
    logging.debug(message)

def load(filename):
    """Loads a json file  and returns a list with data
    Usage: load(filename)"""
    try:
        with open(filename) as json_file:
            json_data = json.load(json_file)
            log_call('load(' + filename + ')')
            return json_data
    except ValueError as e:
        log_call((str(e) +' in database file') , 'warning')
        #log_call('load(' + filename + ') failed. file does not exist.')
    except FileNotFoundError:
        log_call('Database file was not found!', 'warning')

def get_project_count(db):
    """Returns the number of projects in the database
    Usage: get_project_count(database)"""
    num_of_projects = len(db)
    log_call('get_project_count(database) returned' + str(num_of_projects))
    return num_of_projects

def get_project(db, id):
    """Returns the project specified by id
    Usage get_project(database, id)"""
    for each in db:
        if each['project_no'] == id:
            log_call('get_project(database,' + str(id) + ') returned ' + str(len(each)) + ' elements in a list')
            return each
    log_call('get_project(database,' + str(id) + ') returned None')
    return None #If non was found in the loop, return None.

def get_techniques(db):
    """Returns all the techniques used
    Usage: get_techniques(database)"""
    tech_list = []
    for each in db:
        for i in each['techniques_used']:
            tech_list.append(i)
    tech_list = set(tech_list) #Removes all duplicates and stores in tuple
    tech_list = [x for x in tech_list] #Makes the tuple into a list again
    tech_list.sort()
    log_call('get_techniques(database) returned ' + str(len(tech_list))+ ' elements in a list')
    return tech_list

def search(db, sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None):
    """search(db, sort_by='start_date', sort_order='desc', techniques=None, search=None, search_fields=None
    Usage: 
    -"db" should be the database
    -"sort_by" should be the key that you want to sort by
    -"sort_order" should be either 'desc' for descending or 'asc' for ascending
    -"techniques" should be a list of the techniques you want to search in.
    -"search" should be a string, search words seperated with SPACE ex: search='TDP003 2009-08-09'
    -"search_fields" should be a list with the fields you want to search in ex search_fields=['project_name']"""
    #TODO: Dropdown menyer för techniques och search_fields
    log_call('search called')
    project_list = []
    search_list = []
    if search != None: #If any search word has been entered
        search_list = search.lower().split(' ') #List of the searched words seperated with SPACE and in lowercase so that we later can compare ignoring lower/uppercase.
        for each in db: #Iterates through every project in the database
            for item in search_list:
                if check_techniques(techniques, each) or techniques == None: #If techniques exists in 'techniques used' it will continue searching and if techniques used == None it will also continue searching
                    #print([print(str(v).lower()) for v in each.values()])
                    if [str(v).lower() for v in each.values() if item in str(v).lower()] != [] or item in each['techniques_used']: #Checks if item exists as a value in current project, the list comprehension is used so that we ingnores upper/lowercase
                        if search_fields != None: #Check if search_fields is empty, if so each[search_fields].
                            for each_field in search_fields:
                                if [v for v in str(each[each_field]).split(' ') if item == str(v.lower())] != []:
                                    project_list = compare_append(project_list, each)
                        else:#if search fields is empty, it will simply try to append
                            project_list = compare_append(project_list, each)
    elif search_fields == None: # if search still == None it should still find the projects. If search == None, searcb_fields must also be.
        for each in db:
            if check_techniques(techniques, each) or techniques == None: #If techniques exists in 'techniques used' it will continue searching and if techniques used == None it will also continue searching
                project_list = compare_append(project_list, each)

    project_list = sort_project_list(project_list, sort_by, sort_order)
    log_call(('Search ran successfully. Projects found:', len(project_list)))
    return project_list
    
def compare_append(project_list, each):
    """Compares the project list if it already has a certain project in it."""
    if each not in project_list:
        project_list.append(each)
    return project_list


def sort_project_list(project_list, sort_by , sort_order):
    """Sorts the project_list that was found in the search function."""
    if sort_order == 'desc': #This is done so that sorted() can reverse(or not reverse) the sort.
        sort_order = True
    elif sort_order == 'asc':
        sort_order = False
    #Om sorteringen är efter en str ska vi ignorera lowercase annars är det en int vi försöker sortera och då kan vi inte använda lower.
    try: 
        project_list = sorted(project_list, key= lambda k: k[sort_by].lower(), reverse = sort_order)
    except:
        project_list = sorted(project_list, key= lambda k: k[sort_by], reverse = sort_order)
    return project_list


def check_techniques(techniques, each):
    """checks if a technique exists in a project"""
    if techniques == []:#if techniques is empty, it should be ignored and therefore return true.
        return True
    try:
        for each_technique in techniques:
            if each_technique in str(each['techniques_used']):
                return True
    except:
        return False

def get_technique_stats(db):
    """returns a dictionary with all used technique and a short info about the projects that used them"""
    techniques_used = get_techniques(db)
    tech_dict = {key : [] for key in get_techniques(db)}#creates a dict with the wanted structure
    for each_project in db:
        for each_technique in techniques_used:
            if each_technique in each_project['techniques_used']: #If the technique is found within the project
                tech_dict[each_technique] += [{'id' : each_project['project_no'], 'name' : each_project['project_name']}]#adds the project with its info found within the correct technique.
    for tech in tech_dict:
        tech_dict[tech].sort(key = lambda k: k["name"] ) #sorts every technique in the list by the projects names.
    return tech_dict
