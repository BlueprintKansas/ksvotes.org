from wtforms.validators import DataRequired
from flask_babel import lazy_gettext


COUNTIES = ["Allen","Anderson","Atchison","Barber","Barton","Bourbon","Brown","Butler","Chase","Chautauqua","Cherokee","Cheyenne","Clark","Clay","Cloud","Coffey","Comanche","Cowley","Crawford","Decatur","Dickinson","Doniphan","Douglas","Edwards","Elk","Ellis","Ellsworth","Finney","Ford","Franklin","Geary","Gove","Graham","Grant","Gray","Greeley","Greenwood","Hamilton","Harper","Harvey","Haskell","Hodgeman","Jackson","Jefferson","Jewell","Johnson","Kearny","Kingman","Kiowa","Labette","Lane","Leavenworth","Lincoln","Linn","Logan","Lyon","Marion","Marshall","McPherson","Meade","Miami","Mitchell","Montgomery","Morris","Morton","Nemaha","Neosho","Ness","Norton","Osage","Osborne","Ottawa","Pawnee","Phillips","Pottawatomie","Pratt","Rawlins","Reno","Republic","Rice","Riley","Rooks","Rush","Russell","Saline","Scott","Sedgwick","Seward","Shawnee","Sheridan","Sherman","Smith","Stafford","Stanton","Stevens","Sumner","Thomas","Trego","Wabaunsee","Wallace","Washington","Wichita","Wilson","Woodson","Wyandotte"]

def construct_county_choices(default):
    county_list = [('',default)]
    for county in COUNTIES:
        county_list.append((county, county))
    return county_list

def list_of_elections():
    elect_list = [('','')]
    elect_list.append((lazy_gettext('1AB_select_election_primary'), lazy_gettext('1AB_select_election_primary')))
    elect_list.append((lazy_gettext('1AB_select_election_general'), lazy_gettext('1AB_select_election_general')))
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
