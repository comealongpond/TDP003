import json
import logging
import os.path
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
    search_list = search.split(' ') #List of the searched words seperated with SPACE.
    for each in db: #Iterates through every project in the database
        for item in search_list:
            if item in each.values() or item in each['techniques_used']: #Checks if item exists as a value in current project
                print(each['project_name'])
                try: #Check if search_fields is empty, if so each[search_fields] will result in an error and will skip searching with fields.
                    if item in each[search_fields]:# If the search string was found in searched_filed.
                        #project_list = compare_append(project_list, each)
                        project_list.append(each)
                except:
                        project_list.append(each)
                        #project_list = compare_append(project_list, each)
                    # if each[i] in search_list:
                    #    project_list.append(each[i])
    return project_list
    
def compare_append(project_list, each):
    if project_list == []:
        project_list.append(each)
    else:
        for project in project_list:
            if each['project_no'] != project['project_no']:
                project_list.append(each)
    return project_list
