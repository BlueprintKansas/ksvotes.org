from app import db
from datetime import datetime

class ZIPCode(db.Model):
    __tablename__ = 'zipcodes'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    zipcode = db.Column(db.String())
    voter_count = db.Column(db.Integer)
    county_id = db.Column(db.Integer, db.ForeignKey('clerks.id'), nullable=False)

    def save(self, db_session):
        db_session.add(self)
        db_session.commit()

