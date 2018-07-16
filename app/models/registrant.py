import os
from app import db
from datetime import datetime, timedelta
import json
from sqlalchemy.dialects.postgresql import JSON
from cryptography.fernet import Fernet
from sqlalchemy.ext.hybrid import hybrid_property,Comparator
from sqlalchemy.dialects.postgresql import UUID
import uuid
import ksmyvoteinfo


def encryptem(data):
    f = Fernet(os.environ.get("CRYPT_KEY").encode())
    encrypted = f.encrypt(json.dumps(data).encode())
    return encrypted.decode()

def decryptem(data):
    f = Fernet(os.environ.get("CRYPT_KEY").encode())
    return f.decrypt(data.encode())

class Registrant(db.Model):
    __tablename__ = "registrants"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    last_completed_step = db.Column(db.Integer)
    completed_at = db.Column(db.DateTime, default=None)
    session_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4())
    ref = db.Column(db.String())

    #registration steps
    is_citizen = db.Column(db.Boolean, default=False)
    is_eighteen = db.Column(db.Boolean, default=False)
    party = db.Column(db.String()) #enum dem, rep, lib, unaf, green, other
    county = db.Column(db.String()) #may require some geo lookup.
    lang = db.Column(db.String()) #enum? (values?)
    signed_at = db.Column(db.DateTime, default=datetime.utcnow()) #converted to local time on image generated submission
    reg_lookup_complete = db.Column(db.Boolean, default=False)
    addr_lookup_complete = db.Column(db.Boolean, default=False)

    registration = db.Column(db.String())
    #create key from environmental key
    #json stringyify dictionary and encrypt

    @hybrid_property
    def registration_value(self):
        reg = decryptem(self.registration)
        return json.loads(reg.decode())

    @registration_value.setter
    def registration_value(self, data):
        self.registration = encryptem(data)

    class encrypt_comparator(Comparator):
        def operate(self, op, other, **kw):
            return op(
                self.__clause_element__(), encryptem(other),
                **kw
            )

    @registration_value.comparator
    def registration_value(cls):
        return cls.encrypt_comparator(
                    cls.registration
                )

    def update(self, update_payload):
        registration_value = self.registration_value
        for k,v in update_payload.items():
            if k in self.__table__.columns:
                setattr(self, k, v)
            else:
                registration_value[k] = v
        self.registration_value = registration_value


    def has_value_for_req(self, req):
        """
        Given a requirement deterimine if it is a column or a registration value.
        Deterimine if value exists
        """
        if req in self.__table__.columns:
            if not getattr(self, req):
                return False
        else:
            if not self.registration_value.get(req):
                return False
        return True

    def try_value(self, field_name, default_value=''):
        return self.registration_value.get(field_name, default_value)

    def save(self, db_session):
        self.updated_at = datetime.utcnow()
        db_session.add(self)
        db_session.commit()

    @classmethod
    def lookup_by_session_id(cls, sid):
        return cls.query.filter(cls.session_id == sid).first()

    def is_demo(self):
        return True if str(self.session_id) == os.getenv('DEMO_UUID') else False

    @classmethod
    def load_fixtures(cls):
        if not os.getenv('DEMO_UUID'):
            raise Exception("Must defined env var DEMO_UUID")

        r = cls.find_or_create_by(session_id=os.getenv('DEMO_UUID'))
        r.registration_value = {}
        r.update({
            'name_first':   'No',
            'name_middle':  'Such',
            'name_last':        'Person',
            'dob':                    '01/01/2000',
            'addr':         '123 Main St',
            'city':         'Nowhere',
            'state':        'KS',
            'zip':          '12345',
            'email':        'nosuchperson@example.com',
            'phone':        '555-555-1234',
            'identification': 'NONE',
        })
        r.party = 'unaffliated'
        r.reg_lookup_complete = True
        r.addr_lookup_complete = True
        r.is_citizen = True
        r.county = 'TEST'
        r.save(db.session)

    @classmethod
    def find_or_create_by(cls, **kwargs):
        found_one = cls.query.filter_by(**kwargs).first()
        if found_one:
            return found_one
        else:
            r = cls(**kwargs)
            r.registration_value = {}
            r.save(db.session)
            return r

    def middle_initial(self):
        middle_name = self.try_value('name_middle')
        if middle_name and len(middle_name) > 0:
            return middle_name[0]
        else:
            return None

    def name(self):
        return "{} {}".format(self.try_value('name_first'), self.try_value('name_last'))

    def updated_since(self, n_minutes):
        # returns boolean based on comparison of updated_at in last n_minutes
        since_last_updated = datetime.utcnow() - self.updated_at
        window = timedelta(minutes=int(n_minutes))
        if since_last_updated > window:
            return False
        else:
            return True

