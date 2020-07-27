import datetime
import pytz

from dateutil.parser import parse

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
    current_app.logger.debug("req_locale %s - expl_locale %s - def_locale %s" %(req_locale, expl_locale, def_locale))
    # if they differ prefer the explicit
    if expl_locale and expl_locale in LANGUAGES.keys() and req_locale != expl_locale:
        locale = expl_locale
    elif req_locale in LANGUAGES.keys():
        locale = req_locale
    else:
        locale = def_locale
    current_app.logger.debug("using locale %s" %(locale))
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

def primary_election_active(deadline=None, current_time=None):
    """
    Determine if the primary election is active or not

    AB_PRIMARY_DEADLINE env var format is `YYYY-MM-DD HH:MM::SS` assuming a
    Central US time zone.
    """
    # Determine deadline from the environment
    if deadline is None:
        return False

    # Parse our deadline
    local = pytz.timezone("America/Chicago")
    naive = parse(deadline)
    local_dt = local.localize(naive, is_dst=None)
    deadline_utc = local_dt.astimezone(pytz.utc)

    # Determine if we're past deadline
    if current_time is None:
        current_time = datetime.datetime.now(pytz.utc)

    if current_time > deadline_utc:
        return False
    else:
        return True

def list_of_elections():
    from datetime import datetime, timedelta
    import os

    elect_list = []

    # if we are before AB_PRIMARY_DEADLINE
    if primary_election_active(os.getenv('AB_PRIMARY_DEADLINE', None)):
        elect_list.append((lazy_gettext(u'1AB_select_election_primary'), lazy_gettext(u'1AB_select_election_primary')))

    elect_list.append((lazy_gettext(u'1AB_select_election_general'), lazy_gettext(u'1AB_select_election_general')))
    elect_list.append(('permanent', lazy_gettext(u'1AB_select_perm')))
    return elect_list

def is_even_year(year=None):
    """ Determine if it's an even year """
    if year is None:
        today = datetime.date.today()
        year = today.year

    if year % 2 == 0:
        return True
    else:
        return False

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
