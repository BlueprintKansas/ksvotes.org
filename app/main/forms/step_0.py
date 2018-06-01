from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email, Regexp
from flask_babel import gettext

counties = ["Allen","Anderson","Atchison","Barber","Barton","Bourbon","Brown","Butler","Chase","Chautauqua","Cherokee","Cheyenne","Clark","Clay","Cloud","Coffey","Comanche","Cowley","Crawford","Decatur","Dickinson","Doniphan","Douglas","Edwards","Elk","Ellis","Ellsworth","Finney","Ford","Franklin","Geary","Gove","Graham","Grant","Gray","Greeley","Greenwood","Hamilton","Harper","Harvey","Haskell","Hodgeman","Jackson","Jefferson","Jewell","Johnson","Kearny","Kingman","Kiowa","Labette","Lane","Leavenworth","Lincoln","Linn","Logan","Lyon","Marion","Marshall","McPherson","Meade","Miami","Mitchell","Montgomery","Morris","Morton","Nemaha","Neosho","Ness","Norton","Osage","Osborne","Ottawa","Pawnee","Phillips","Pottawatomie","Pratt","Rawlins","Reno","Republic","Rice","Riley","Rooks","Rush","Russell","Saline","Scott","Sedgwick","Seward","Shawnee","Sheridan","Sherman","Smith","Stafford","Stanton","Stevens","Sumner","Thomas","Trego","Wabaunsee","Wallace","Washington","Wichita","Wilson","Woodson","Wyandotte"]
class FormStep0(FlaskForm):
    name_first = StringField(gettext('0_first'), validators=[DataRequired(message=gettext('Required'))])
    name_last = StringField(gettext('0_last'), validators=[DataRequired(message=gettext('Required'))])
    dob = StringField(gettext('0_dob'), validators=[DataRequired(message=gettext('Required'))])
    county = SelectField(gettext('0_county'),
                         validators=[DataRequired(message=gettext('Required'))],
                         choices=[(c, c) for c in counties]
                         )
    email = StringField(gettext('0_email'), validators=[DataRequired(message=gettext('Required')), Email(message=gettext('0_email_flag'))])
    phone = StringField(gettext('0_phone'), validators=[Regexp('^\w+$', message=gettext('0_phone_help'))])
