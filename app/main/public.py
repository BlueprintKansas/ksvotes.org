from app.main import main
from flask import g, url_for, render_template

#step 0 / 0x
@main.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

#step 1
@main.route('/citizenship')
def citizenship():
    return 'citizenship'

#step 2
@main.route('/name')
def name():
    return 'name'

#step 3
@main.route('/address')
def address():
    return 'address'

#step 4
@main.route('/party')
def party():
    #return normalized address
    return 'party'

#step 5 (4? 4.5?)
@main.route('/identification')
def identification():
    return 'identification'

#step 6 NVRIS preview
@main.route('/preview')
def preview():
    # include signing box
    return 'preview'

#step 7 (affirm signature) (redirec if desktop?)
@main.route('/affirmation')
def affirmation():
    return "affirmation"

#step 8 confirmation reciept and next steps (share?)
@main.route('/confirmation')
def confirmation():
    return 'confirmation'
