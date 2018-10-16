from app.models import *
import json
def test_db_connection(app, db_session, client):
    genq = db_session.query(Registrant).first()
    assert genq == None

def test_insert_get_clerk(app, db_session, client):
    new_clerk = Clerk(
        county = "foo",
        officer = "bar",
        email = "foo@bar.com",
        phone = "5555555555",
        fax = "5555555555",
        address1 = "123 fake st",
        address2 = "ste 107",
        city = "springfield",
        state = "KANSAS",
        zip = "55555",
    )
    db_session.add(new_clerk)
    db_session.commit()
    clerk = Clerk.find_by_county('foo')
    assert clerk.officer == 'bar'

def test_insert_get_registrant_start(app, db_session, client):
    #data should be dictionary
    registrant_data = {
        "name_first": "foo",
        "name_last": "bar",
        "dob": "01-01-2018",
        "email": "foo@bar.com",
        "phone": "555-555-5555"
    }
    #registration value should be automatically encrypted and decrypted
    new_registrant = Registrant(
        lang='en',
        county="Johnson",
        registration_value = registrant_data,
    )
    db_session.add(new_registrant)
    db_session.commit()


    registrant = db_session.query(Registrant).first()
    #confirm that registration was modified from dictionary value
    assert isinstance(registrant.registration, (dict)) == False

    #confirm that registration_value is returned decrypted and marshalled to dictionary
    assert isinstance(registrant.registration_value, (dict)) == True
    assert registrant.registration_value.get('name_first') == "foo"

    #confirm that registration was encrypted and can be decrypted
    decrypted = json.loads(decryptem(registrant.registration))
    assert decrypted.get('name_first') == "foo"

    #query by uuid
    registrant_uuid = db_session.query(Registrant).filter_by(session_id=registrant.session_id).first()
    assert registrant_uuid.registration_value.get('name_first') == "foo"

def test_prepopulate_address(app, db_session, client):
    sosrec = { 'Address': '123 Main St #456 Wichita, KS, 12345', 'Party': 'Republican' }
    r = Registrant()
    r.populate_address(sosrec)

    assert r.try_value('addr') == '123 Main St'
    assert r.try_value('unit') == '# 456'
    assert r.try_value('city') == 'Wichita'
    assert r.try_value('state') == 'KS'
    assert r.try_value('zip') == '12345'

