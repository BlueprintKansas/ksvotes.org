from app.models import *
from flask import g
def create_registrant(session):
    registrant = Registrant(
        registration_value={
            "name_first": "foo",
            "name_last": "bar",
            "dob":"01/01/2000",
            "email":"foo@example.com",
        },
        county="Douglas",
        reg_lookup_complete = True,
    )
    session.add(registrant)
    session.commit()
    return registrant


def test_citizenship_not_checked_does_not_return_redirect(app, session, client):
    """
    An existing user tries to update their record, but does not select the citizen checkbox
    """
    registrant = create_registrant(session)
    with client.session_transaction() as sess:
        sess['session_id'] = str(registrant.session_id)

    form_payload = {}
    response = client.post('/vr/citizenship', data=form_payload, follow_redirects=False)
    assert response.status_code != 302

def test_citizenship_checked_returns_redirect(app,session,client):
    registrant = create_registrant(session)
    with client.session_transaction() as sess:
        sess['session_id'] = str(registrant.session_id)

    form_payload = {"is_citizen": True}

    response = client.post('/vr/citizenship', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/vr/name' in redirect_data) == True
