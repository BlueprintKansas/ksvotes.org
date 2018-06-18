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
            "zip": "66044"
        },
        county="Douglas",
        reg_lookup_complete = True,
        addr_lookup_complete = True,
        is_citizen=True
    )
    db_session.add(registrant)
    db_session.commit()
    return registrant


def test_vr_4_no_party_provided(app, db_session, client):
    """
    An existing user tries to update their record, but does not provide a name field
    """
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session["session_id"] = str(registrant.session_id)

    form_payload = {}
    response = client.post("/vr/party", data=form_payload, follow_redirects=False)
    assert response.status_code != 302

def test_valid_vr_4_returns_redirect(app,db_session,client):
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session["session_id"] = str(registrant.session_id)

    form_payload = {"party": "unafilliated"}

    response = client.post("/vr/party", data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ("/vr/identification" in redirect_data) == True
