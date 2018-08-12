from app import db
from datetime import datetime

class ZIPCodeCounty(db.Model):
    __tablename__ = 'zipcode_counties'

    clerk_id = db.Column(db.Integer, db.ForeignKey('clerks.id'), nullable=False, primary_key=True)
    zipcode_id = db.Column(db.Integer, db.ForeignKey('zipcodes.id'), nullable=False, primary_key=True)
    voter_count = db.Column(db.Integer)
    zipcode = db.relationship('ZIPCode')
    county = db.relationship('Clerk')

    def save(self, db_session):
        db_session.add(self)
        db_session.commit()


class ZIPCode(db.Model):
    __tablename__ = 'zipcodes'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    zipcode = db.Column(db.String(), unique=True)
    counties = db.relationship('ZIPCodeCounty')

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
    def find_by_zip5(cls, zip5):
        return cls.query.filter(cls.zipcode == zip5).first()

    @classmethod
    def guess_county(cls, zip5):
        z = cls.query.filter(cls.zipcode == zip5).first()
        if not z:
            return None
        if len(z.counties) == 1:
            return z.counties[0].county.county

        # more than one county for this ZIP5.
        # sort the list by voter_count and pick the biggest.
        sorted_by_voter_count = sorted(z.counties, key=lambda zc: zc.voter_count, reverse=True)
        return sorted_by_voter_count[0].county.county

    @classmethod
    def load_fixtures(cls):
        import os
        import csv
        from app.models import Clerk

        ZIPCodeCounty.query.delete() # drop all m2m rows to start fresh

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
                db.session.add(z)
                zc = ZIPCodeCounty(voter_count=row[2], county=clerk)
                z.counties.append(zc)

        db.session.commit() # single transaction at end

