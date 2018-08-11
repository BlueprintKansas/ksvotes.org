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

    @classmethod
    def find_or_create_by(cls, **kwargs):
        found_one = cls.query.filter_by(**kwargs).first()
        if found_one:
            return found_one
        else:
            z = cls(**kwargs)
            return z

    @classmethod
    def load_fixtures(cls):
        import os
        import csv
        from app.models import Clerk

        csv_file = 'ks-zip-by-county.csv'
        with open(csv_file, newline="\n") as csvfile:
            next(csvfile)  # skip headers
            # zip5,county_name,voter_count
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                zip5 = row[0]
                clerk = Clerk.find_by_county(row[1])
                if not clerk:
                    raise Exception("Failed to find county for %s" %(row[1]))

                z = ZIPCode.find_or_create_by(zipcode=zip5)
                z.county_id = clerk.id
                z.voter_count = row[2]
                z.save(db.session)

