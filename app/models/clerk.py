from app import db
from datetime import datetime

class Clerk(db.Model):
    __tablename__ = "clerks"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
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

    def save(self, db_session):
        db_session.add(self)
        db_session.commit()

    @classmethod
    def find_by_county(cls, county_name):
        if not county_name or len(county_name) == 0:
            return None
        return cls.query.filter(cls.county == county_name).first()

    @classmethod
    def find_or_create_by(cls, **kwargs):
        found_one = cls.query.filter_by(**kwargs).first()
        if found_one:
            return found_one
        else:
            clerk = cls(**kwargs)
            return clerk

    @classmethod
    def load_fixtures(cls):
        import os
        import csv
        from flask import current_app
        csv_file = 'county-clerks.csv'
        with open(csv_file, newline="\n") as csvfile:
            next(csvfile)  # skip headers
            # GEOCODE_FORMAT,COUNTY,OFFICER,EMAIL,HOURS,PHONE,FAX,ADDRESS1,ADDRESS2,CITY,STATE,ZIP
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                ucfirst_county = row[1][0] + row[1][1:].lower()
                if ucfirst_county == 'Mcpherson':
                    ucfirst_county = 'McPherson'
                clerk = Clerk.find_or_create_by(county=ucfirst_county)
                clerk.officer = row[2]
                clerk.email = row[3]
                clerk.phone = row[5]
                clerk.fax = row[6]
                clerk.address1 = row[7]
                clerk.address2 = row[8]
                clerk.city = row[9]
                clerk.state = row[10]
                clerk.zip = row[11]
                clerk.save(db.session)
    
        # add the TEST fixture
        test_clerk = Clerk.find_or_create_by(county='TEST')
        test_clerk.email = 'registration@ksvotes.org'
        test_clerk.phone = 'test'
        test_clerk.fax = 'test'
        test_clerk.officer = 'test'
        test_clerk.address1 = 'test'
        test_clerk.city = 'test'
        test_clerk.state = 'KS'
        test_clerk.zip = 'test'
        test_clerk.save(db.session)
