from wtforms.validators import DataRequired
from flask_babel import lazy_gettext
from flask import request, g, current_app
from config import LANGUAGES

COUNTIES = ["Allen","Anderson","Atchison","Barber","Barton","Bourbon","Brown","Butler","Chase","Chautauqua","Cherokee","Cheyenne","Clark","Clay","Cloud","Coffey","Comanche","Cowley","Crawford","Decatur","Dickinson","Doniphan","Douglas","Edwards","Elk","Ellis","Ellsworth","Finney","Ford","Franklin","Geary","Gove","Graham","Grant","Gray","Greeley","Greenwood","Hamilton","Harper","Harvey","Haskell","Hodgeman","Jackson","Jefferson","Jewell","Johnson","Kearny","Kingman","Kiowa","Labette","Lane","Leavenworth","Lincoln","Linn","Logan","Lyon","Marion","Marshall","McPherson","Meade","Miami","Mitchell","Montgomery","Morris","Morton","Nemaha","Neosho","Ness","Norton","Osage","Osborne","Ottawa","Pawnee","Phillips","Pottawatomie","Pratt","Rawlins","Reno","Republic","Rice","Riley","Rooks","Rush","Russell","Saline","Scott","Sedgwick","Seward","Shawnee","Sheridan","Sherman","Smith","Stafford","Stanton","Stevens","Sumner","Thomas","Trego","Wabaunsee","Wallace","Washington","Wichita","Wilson","Woodson","Wyandotte","TEST"]

KS_DL_PATTERN = '^(\w\d\w\d\w|K\d\d-\d\d-\d\d\d\d|\d\d\d-\d\d-\d\d\d\d)$'

def guess_locale():
    req_locale = request.accept_languages.best_match(LANGUAGES.keys())
    expl_locale = g.get('lang_code')
    def_locale = g.get('lang_code', current_app.config['BABEL_DEFAULT_LOCALE'])
    if def_locale not in LANGUAGES.keys():
        def_locale = current_app.config['BABEL_DEFAULT_LOCALE'] # fix recursive 404 error
    current_app.logger.info("req_locale %s - expl_locale %s - def_locale %s" %(req_locale, expl_locale, def_locale))
    # if they differ prefer the explicit
    if expl_locale and expl_locale in LANGUAGES.keys() and req_locale != expl_locale:
        locale = expl_locale
    elif req_locale in LANGUAGES.keys():
        locale = req_locale
    else:
        locale = def_locale
    current_app.logger.info("using locale %s" %(locale))
    return locale

def construct_county_choices(default):
    county_list = [('','')]
    for county in COUNTIES:
        county_list.append((county, county))
    return county_list

def parse_election_date(election):
    import re
    import dateparser
    pattern = '(Primary|Primaria|General) \((.+)\)'
    m = re.match(pattern, str(election))
    if not m:
        return None
    date = m.group(2)
    return dateparser.parse(date)

def list_of_elections():
    from datetime import datetime, timedelta
    import os

    elect_list = []

    # if we are at least 7 days before the primary, include it.
    today = datetime.utcnow()
    primary_date = parse_election_date(lazy_gettext(u'1AB_select_election_primary'))
    window = timedelta(days=int(os.getenv('AB_DAYS_BEFORE_PRIMARY', default=7)))

    if primary_date and (primary_date - today) > window:
        elect_list.append((lazy_gettext(u'1AB_select_election_primary'), lazy_gettext(u'1AB_select_election_primary')))

    elect_list.append((lazy_gettext(u'1AB_select_election_general'), lazy_gettext(u'1AB_select_election_general')))
    elect_list.append(('permanent', lazy_gettext(u'1AB_select_perm')))
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
