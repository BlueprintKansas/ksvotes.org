from wtforms.validators import DataRequired
from flask_babel import lazy_gettext
from flask import request, g, current_app
from config import LANGUAGES

COUNTIES = ["Allen","Anderson","Atchison","Barber","Barton","Bourbon","Brown","Butler","Chase","Chautauqua","Cherokee","Cheyenne","Clark","Clay","Cloud","Coffey","Comanche","Cowley","Crawford","Decatur","Dickinson","Doniphan","Douglas","Edwards","Elk","Ellis","Ellsworth","Finney","Ford","Franklin","Geary","Gove","Graham","Grant","Gray","Greeley","Greenwood","Hamilton","Harper","Harvey","Haskell","Hodgeman","Jackson","Jefferson","Jewell","Johnson","Kearny","Kingman","Kiowa","Labette","Lane","Leavenworth","Lincoln","Linn","Logan","Lyon","Marion","Marshall","McPherson","Meade","Miami","Mitchell","Montgomery","Morris","Morton","Nemaha","Neosho","Ness","Norton","Osage","Osborne","Ottawa","Pawnee","Phillips","Pottawatomie","Pratt","Rawlins","Reno","Republic","Rice","Riley","Rooks","Rush","Russell","Saline","Scott","Sedgwick","Seward","Shawnee","Sheridan","Sherman","Smith","Stafford","Stanton","Stevens","Sumner","Thomas","Trego","Wabaunsee","Wallace","Washington","Wichita","Wilson","Woodson","Wyandotte"]

def guess_locale():
    req_locale = request.accept_languages.best_match(LANGUAGES.keys())
    expl_locale = g.get('lang_code')
    def_locale = g.get('lang_code', current_app.config['BABEL_DEFAULT_LOCALE'])
    current_app.logger.info("req_locale %s - expl_locale %s - def_locale %s" %(req_locale, expl_locale, def_locale))
    # if they differ prefer the explicit
    if expl_locale and req_locale != expl_locale:
        locale = expl_locale
    else:
        locale = req_locale or def_locale
    current_app.logger.info("using locale %s" %(locale))
    return locale

def construct_county_choices(default):
    county_list = [('',default)]
    for county in COUNTIES:
        county_list.append((county, county))
    return county_list

def list_of_elections():
    elect_list = [('','')]
    elect_list.append((lazy_gettext(u'1AB_select_election_primary'), lazy_gettext(u'1AB_select_election_primary')))
    elect_list.append((lazy_gettext(u'1AB_select_election_general'), lazy_gettext(u'1AB_select_election_general')))
    return elect_list

class RequiredIfBool(DataRequired):
    def __init__(self, check, *args, **kwargs):
        self.check = check
        super(RequiredIfBool, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        check_field = form._fields.get(self.check)
        if check_field is None:
            raise Exception('invalid field' % self.check)
        if bool(check_field.data):
            super(RequiredIfBool, self).__call__(form, field)
