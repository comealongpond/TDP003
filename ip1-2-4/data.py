import json
import logging
import os.path
import operator

def log_call(message):
    """Logs message into a logfile
    Usage: log_call(message)"""
    logger = logging.getLogger('datalog')
    if os.path.isfile('datalog.log'):  
        logger.info(message)
    else: #If log-file does not exists, it will create a new one.
        hdlr = logging.FileHandler('datalog.log') #creates the file
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)
        logger.info(message)

def load(filename):
    """Loads and returns a data file
    Usage: load(filename)"""
    try:
        with open(filename) as json_file:
            json_data = json.load(json_file)
            log_call('load(' + filename + ')')
            return json_data
    except:
        log_call('load(' + filename + ') failed. file does not exist.')
        pass

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
    #TODO: Dropdown menyer för techniques och search_fields
    log_call('search called')
    project_list = []
    if search == None:
        log_call('Search failed. No given string.')
        return 'Nothing entered in the search field.'
    search_list = search.split(' ') #List of the searched words seperated with SPACE.
    for each in db: #Iterates through every project in the database
        for item in search_list:
            if check_techniques(techniques, each) or techniques == None: #If techniques exists in 'techniques used' it will continue searching and if techniques used == None it will also continue searching
                if item in each.values() or item in each['techniques_used']: #Checks if item exists as a value in current project
                    if search_fields != None: #Check if search_fields is empty, if so each[search_fields].
                        if item in each[search_fields]:# If the search string was found in searched_filed.
                            project_list = compare_append(project_list, each)
                    else:
                        project_list = compare_append(project_list, each)
    project_list = sort_project_list(project_list, sort_by, sort_order)
    log_call(('Search ran successfully. Projects found:', len(project_list)))
    return project_list
    
def compare_append(project_list, each):
    """Compares the project list if it already has a certain project in it."""
    if each not in project_list:
        project_list.append(each)
    log_call('compare_append(project_list, each) called from search()')
    return project_list


def sort_project_list(project_list, sort_by , sort_order):
    """Sorts the project_list that was found in the search function."""
    if sort_order == 'desc': #This is done so that sorted() can reverse(or not reverse) the sort.
        sort_order = True
    elif sort_order == 'asc':
        sort_order = False
    project_list = sorted(project_list, key=operator.itemgetter(sort_by), reverse=sort_order) #sorts the project_list by "sort_by". reverse makes the sort order reverse or not.
    log_call('sort_project_list(project_list, sort_by , sort_order) called from search()')
    return project_list


def check_techniques(techniques, each):
    """checks if a technique exists in a project"""
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
        tech_dict[tech].sort(key = lambda : l["name"] ) #sorts every technique in the list by the projects names.
    return tech_dict
