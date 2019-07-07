from app.models import *
from app.main.helpers import is_even_year
from datetime import datetime

def create_registrant(db_session):
    registrant = Registrant(
        registration_value={
            "name_first": "foo",
            "name_last": "bar",
            "dob":"01/01/2000",
            "email":"foo@example.com",
        },
        county="TEST",
        reg_lookup_complete = True
    )
    db_session.add(registrant)
    db_session.commit()
    return registrant

def test_ab_1_general_election(app, db_session, client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {
      "elections": "General"
    }
    response = client.post('/ab/election_picker', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/ab/address' in redirect_data) == True

def test_ab_1_general_election_already_registered(app, db_session, client):
    registrant = create_registrant(db_session)
    registrant.vr_completed_at = datetime.utcnow()
    registrant.save(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {
      "elections": "General"
    }
    response = client.post('/ab/election_picker', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/ab/identification' in redirect_data) == True

def test_ab_1_general_and_primary_no_party(app, db_session, client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {
      "elections": ['General', 'Primary']
    }

    response = client.post('/ab/election_picker', data=form_payload, follow_redirects=False)
    if is_even_year():
        assert response.status_code != 302
    else:
        assert response.status_code == 302

def test_ab_1_general_and_primary_with_party(app, db_session, client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {
      "elections": ['General', 'Primary'],
      "party": 'Republican'
    }

    response = client.post('/ab/election_picker', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/ab/address' in redirect_data) == True

def test_ab_1_permanent_no_party(app, db_session, client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {
      "elections": ['permanent'],
      "perm_reason": 'some reason',
    }

    response = client.post('/ab/election_picker', data=form_payload, follow_redirects=False)
    assert response.status_code == 302
    redirect_data = response.data.decode()
    assert ('/ab/address' in redirect_data) == True

def test_ab_1_permanent_no_reason(app, db_session, client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {
      "elections": ['permanent'],
      "party": 'Republican',
    }

    response = client.post('/ab/election_picker', data=form_payload, follow_redirects=False)
    assert response.status_code != 302


def test_ab_1_permanent_with_party_and_reason(app, db_session, client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {
      "elections": ['permanent'],
      "party": 'Republican',
      "perm_reason": 'some reason',
    }

    response = client.post('/ab/election_picker', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/ab/address' in redirect_data) == True

