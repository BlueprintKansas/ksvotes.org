from app.models import *
from app.main.VR.example_form import signature_img_string

def create_registrant(db_session):
    registrant = Registrant(
        registration_value={
            "name_first": "foo",
            "name_last": "bar",
            "dob":"01/01/2000",
            "email":"foo@example.com",
            "addr": "707 Vermont St",
            "unit": "Room A",
            "city": "Lawrence",
            "state": "KANSAS",
            "zip": "66044",
            "identification": "nnnnn",
            "elections": "General (11/7/2018)",
        },
        county="Douglas",
        reg_lookup_complete = True,
        addr_lookup_complete = True,
        is_citizen=True,
        party="unafilliated"
    )
    db_session.add(registrant)
    db_session.commit()
    return registrant


def test_ab_6_no_signature_provided(app, db_session, client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {}
    response = client.post('/ab/preview', data=form_payload, follow_redirects=False)
    assert response.status_code != 302

def test_ab_6_bad_signature_provided(app, db_session, client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {'signature_string' : 'foobar'}
    response = client.post('/ab/preview', data=form_payload, follow_redirects=False)
    assert response.status_code != 302

def test_valid_ab_6_returns_redirect(app,db_session,client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {"signature_string": signature_img_string}

    response = client.post('/ab/preview', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/ab/affirmation' in redirect_data) == True

