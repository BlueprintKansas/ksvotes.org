import os
from app import db
from datetime import datetime, timedelta
import pytz
import json
from sqlalchemy.dialects.postgresql import JSON
from cryptography.fernet import Fernet
from sqlalchemy.ext.hybrid import hybrid_property,Comparator
from sqlalchemy.dialects.postgresql import UUID
import uuid
import ksmyvoteinfo
import usaddress

def encryptem(data):
    f = Fernet(os.environ.get("CRYPT_KEY").encode())
    encrypted = f.encrypt(json.dumps(data).encode())
    return encrypted.decode()

def decryptem(data):
    f = Fernet(os.environ.get("CRYPT_KEY").encode())
    if not data:
        return {}
    return f.decrypt(data.encode())

class Registrant(db.Model):
    __tablename__ = "registrants"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    redacted_at = db.Column(db.DateTime, default=None)
    vr_completed_at = db.Column(db.DateTime, default=None)
    ab_completed_at = db.Column(db.DateTime, default=None)
    ab_permanent = db.Column(db.Boolean, default=None)
    session_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4())
    ref = db.Column(db.String())

    #registration steps
    is_citizen = db.Column(db.Boolean, default=None)
    is_eighteen = db.Column(db.Boolean, default=None)
    dob_year = db.Column(db.Integer)
    party = db.Column(db.String())
    county = db.Column(db.String())
    lang = db.Column(db.String())
    signed_at = db.Column(db.DateTime, default=datetime.utcnow)
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

    # update() is set_value() for a dict (bulk) to save encrypt/decrypt overhead
    def update(self, update_payload):
        rval = {}
        if self.registration:
          rval = self.registration_value
        for k,v in update_payload.items():
            if k in self.__table__.columns:
                setattr(self, k, v)
            else:
                rval[k] = v
        self.registration_value = rval

    def set_value(self, name, value):
        if name in self.__table__.columns:
            return super().__setattr__(name, value)
        else:
            rval = {}
            if self.registration:
                rval = self.registration_value
            rval[name] = value
            self.registration_value = rval
            return self

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

    def try_clerk(self):
        from app.models import Clerk
        return Clerk.find_by_county(self.county)

    def get_dob_year(self):
        dob_dt = datetime.strptime(self.try_value('dob'), '%m/%d/%Y')
        return int(dob_dt.year)

    def save(self, db_session):
        self.updated_at = datetime.utcnow()
        db_session.add(self)
        db_session.commit()

    def best_zip5(self):
        validated_addr = self.try_value('validated_addresses')
        if validated_addr and 'current_address' in validated_addr and 'zip5' in validated_addr['current_address']:
            return validated_addr['current_address']['zip5']
        return self.try_value('zip')

    def precinct_address(self):
        parts = []
        parts.append(self.try_value('addr'))
        parts.append(self.try_value('city'))
        parts.append(self.try_value('state'))
        parts.append(self.try_value('zip'))
        return ' '.join(parts)

    @classmethod
    def lookup_by_session_id(cls, sid):
        return cls.query.filter(cls.session_id == sid).first()

    @classmethod
    def find_by_session(cls, sid):
        return cls.lookup_by_session_id(sid)

    def is_demo(self):
        return True if str(self.session_id) == os.getenv('DEMO_UUID') else False

    @classmethod
    def load_fixtures(cls):
        if not os.getenv('DEMO_UUID'):
            raise Exception("Must defined env var DEMO_UUID")

        r = cls.find_or_create_by(session_id=os.getenv('DEMO_UUID'))
        r.registration_value = {}
        r.update({
            'name_first': 'No',
            'name_middle': 'Such',
            'name_last': 'Person',
            'dob': '01/01/2000',
            'addr': '123 Main St',
            'city': 'Nowhere',
            'state': 'KS',
            'zip': '12345',
            'email': 'nosuchperson@example.com',
            'phone': '555-555-1234',
            'identification': 'NONE',
        })
        r.party = 'Unaffiliated'
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

    @classmethod
    def for_each(cls, func, *where):
        res = cls.query.filter(*where).yield_per(200).enable_eagerloads(False)
        for r in res:
            func(r)

    @classmethod
    def redact(cls, reg):
        fields = ['identification', 'ab_identification', 'vr_form', 'ab_forms', 'signature_string']
        for f in fields:
            reg.set_value(f, None)
        reg.redacted_at = datetime.utcnow()
        db.session.add(reg)
        db.session.flush()

    @classmethod
    def redact_pii(cls, before_when):
        cls.for_each(cls.redact, cls.updated_at <= before_when, cls.redacted_at == None)
        db.session.commit()

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

    def elections(self):
        return self.try_value('elections').split('|')

    def sign_ab_forms(self):
        sig_string = self.try_value('signature_string', None)
        if not sig_string:
            return False

        from app.services.nvris_client import NVRISClient
        nvris_client = NVRISClient(self)
        ab_forms = []
        for election in self.elections():
            signed_ab_form = nvris_client.get_ab_form(election)
            if signed_ab_form:
                ab_forms.append(signed_ab_form)

        if len(ab_forms) > 0:
            self.update({'ab_forms':ab_forms})
            self.signed_at = datetime.utcnow()

        return ab_forms

    def signed_at_central_tz(self):
        utc_tz = pytz.timezone('UTC')
        central_tz = pytz.timezone('US/Central')
        signed_at_utc = utc_tz.localize(self.signed_at)
        return signed_at_utc.astimezone(central_tz)

    def populate_address(self, sosrec):
        address = sosrec['Address'].replace('<br/>', ' ')
        addr_parts = usaddress.tag(address)
        payload = {
          'addr': "",
          'unit': "",
          'city': "",
          'state': "",
          'zip': ""
        }
        for key, val in addr_parts[0].items():
            if key == 'OccupancyIdentifier':
                payload['unit'] = val
            elif key == 'PlaceName':
                payload['city'] = val
            elif key == 'StateName':
                payload['state'] = val
            elif key == 'ZipCode':
                payload['zip'] = val
            else:
                if len(payload['addr']) > 0:
                    payload['addr'] = ' '.join([payload['addr'], val])
                else:
                    payload['addr'] = val

        self.update(payload)

