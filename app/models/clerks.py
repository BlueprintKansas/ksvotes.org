from app import db
from datetime import datetime

class ClerksModel(db.Model):
    __tablename__ = "clerks"

    id = db.Column(db.Integer, primary_key=True)
    county = db.Column(db.String()) #enum of ks counties
    officer = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String()) #formatted NNNNNNNNNN
    fax = db.Column(db.String()) #formatted NNNNNNNNNN
    address1 = db.Column(db.String())
    address2 = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String(), default='KS')
    zip = db.Column(db.String())
