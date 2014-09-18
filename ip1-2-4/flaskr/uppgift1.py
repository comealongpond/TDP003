personlist = [{'name' :'Edling Erik','address':'Huggarvägen 45','birthdate':'19940428'},{'name' :'Carlsson Anton','address':'Herrjungavägen 2','birthdate':'19920828'},{'name' :'Adling Frank','address':'bjursätragatan 37','birthdate':'19600722'}]
def format_by(keyn, personlist):
    personlist = sorted(personlist, key=lambda k: k[keyn])
    for each in personlist:
        print(each[keyn])
    return personlist

