from app.models import *

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
            "elections": "General"
        },
        county="TEST",
        reg_lookup_complete = True,
        addr_lookup_complete = True,
        is_citizen=True,
    )
    registrant.save(db_session)
    return registrant


def test_ab_5_no_id_provided_ok(app, db_session, client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {}
    response = client.post('/ab/identification', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/ab/preview' in redirect_data) == True

def test_invalid_ab_5_reloads_form(app,db_session,client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {"ab_identification": "nnnnn"}

    response = client.post('/ab/identification', data=form_payload, follow_redirects=False)
    assert response.status_code != 302

def test_valid_ab_5_redirects_to_preview(app,db_session,client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {"ab_identification": "K00-00-0000"}

    response = client.post('/ab/identification', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/ab/preview' in redirect_data) == True
