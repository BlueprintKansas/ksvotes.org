from app.main import main
from flask import g, url_for, render_template, jsonify, request
import time
#step 0 / 0x


@main.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        time.sleep(5)
        return jsonify({"post": "success"})

    counties = ["Allen","Anderson","Atchison","Barber","Barton","Bourbon","Brown","Butler","Chase","Chautauqua","Cherokee","Cheyenne","Clark","Clay","Cloud","Coffey","Comanche","Cowley","Crawford","Decatur","Dickinson","Doniphan","Douglas","Edwards","Elk","Ellis","Ellsworth","Finney","Ford","Franklin","Geary","Gove","Graham","Grant","Gray","Greeley","Greenwood","Hamilton","Harper","Harvey","Haskell","Hodgeman","Jackson","Jefferson","Jewell","Johnson","Kearny","Kingman","Kiowa","Labette","Lane","Leavenworth","Lincoln","Linn","Logan","Lyon","Marion","Marshall","McPherson","Meade","Miami","Mitchell","Montgomery","Morris","Morton","Nemaha","Neosho","Ness","Norton","Osage","Osborne","Ottawa","Pawnee","Phillips","Pottawatomie","Pratt","Rawlins","Reno","Republic","Rice","Riley","Rooks","Rush","Russell","Saline","Scott","Sedgwick","Seward","Shawnee","Sheridan","Sherman","Smith","Stafford","Stanton","Stevens","Sumner","Thomas","Trego","Wabaunsee","Wallace","Washington","Wichita","Wilson","Woodson","Wyandotte"]
    return render_template('index.html', counties=counties)

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

#step 7 (affirm signature) (redirect if desktop?)
@main.route('/affirmation')
def affirmation():
    return "affirmation"

#step 8 confirmation reciept and next steps (share?)
@main.route('/confirmation')
def confirmation():
    return 'confirmation'
