from app.main import main
from flask import g, url_for, render_template, jsonify, request
import time
from app.main.forms import *
#step 0 / 0x


@main.route('/', methods=["GET", "POST"])
def index():
    form = FormStep0()
    if request.method == "POST" and form.validate_on_submit():
        # do all the logic
        data = request.get_json()
        print(data)
        time.sleep(5)
        return jsonify({"post": "success"})

    counties = ["Allen","Anderson","Atchison","Barber","Barton","Bourbon","Brown","Butler","Chase","Chautauqua","Cherokee","Cheyenne","Clark","Clay","Cloud","Coffey","Comanche","Cowley","Crawford","Decatur","Dickinson","Doniphan","Douglas","Edwards","Elk","Ellis","Ellsworth","Finney","Ford","Franklin","Geary","Gove","Graham","Grant","Gray","Greeley","Greenwood","Hamilton","Harper","Harvey","Haskell","Hodgeman","Jackson","Jefferson","Jewell","Johnson","Kearny","Kingman","Kiowa","Labette","Lane","Leavenworth","Lincoln","Linn","Logan","Lyon","Marion","Marshall","McPherson","Meade","Miami","Mitchell","Montgomery","Morris","Morton","Nemaha","Neosho","Ness","Norton","Osage","Osborne","Ottawa","Pawnee","Phillips","Pottawatomie","Pratt","Rawlins","Reno","Republic","Rice","Riley","Rooks","Rush","Russell","Saline","Scott","Sedgwick","Seward","Shawnee","Sheridan","Sherman","Smith","Stafford","Stanton","Stevens","Sumner","Thomas","Trego","Wabaunsee","Wallace","Washington","Wichita","Wilson","Woodson","Wyandotte"]
    return render_template('index.html', counties=counties, form = form)

#step 1
@main.route('/citizenship', methods=["GET", "POST"])
def citizenship():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        time.sleep(5)
        return jsonify({"post": "success"})
    return render_template('citizenship.html')

#step 2
@main.route('/name', methods=["GET", "POST"])
def name():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        time.sleep(5)
        return jsonify({"post": "success"})
    return render_template('name.html')

#step 3
@main.route('/address', methods=["GET", "POST"])
def address():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        time.sleep(5)
        return jsonify({"post": "success"})
    return render_template('address.html')

#step 4
@main.route('/party', methods=["GET", "POST"])
def party():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        time.sleep(5)
        return jsonify({"post": "success"})
    return render_template('party.html')

#step 5 (4? 4.5?)
@main.route('/identification', methods=["GET", "POST"])
def identification():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        time.sleep(5)
        return jsonify({"post": "success"})
    return render_template('identification.html')

#step 6 NVRIS preview
@main.route('/preview')
def preview():
    # include signing box
    return 'preview'

#step 7 (affirm signature) (redirect if desktop?)
@main.route('/affirmation')
def affirmation():
    return "affirmation"

#step 8 confirmation reciept and next steps (share?)
@main.route('/confirmation')
def confirmation():
    return 'confirmation'
