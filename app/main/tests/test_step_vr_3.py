from app.models import *


def create_registrant(db_session):
    registrant = Registrant(
        registration_value={
            "name_first": "foo",
            "name_last": "bar",
            "dob":"01/01/2000",
            "email":"foo@example.com",
        },
        county="Douglas",
        reg_lookup_complete = True,
        is_citizen=True
    )
    db_session.add(registrant)
    db_session.commit()
    return registrant


def test_vr_3_no_address_provided(app, db_session, client):
    """
    An existing user tries to post without an address provided
    """

    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {}
    response = client.post('/vr/address', data=form_payload, follow_redirects=False)
    assert response.status_code != 302


def test_vr_3_single_valid_address(app, db_session, client):
    """
    An existing user provides a valid address, but no previous address or mailing address.
    """

    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {
        'addr': "707 Vermont St",
        'unit': "Room A",
        'city': "Lawrence",
        'state': "KANSAS",
        'zip': '66044'
    }

    response = client.post('/vr/address', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/vr/party' in redirect_data) == True

    updated_registrant = db_session.query(Registrant).filter_by(session_id = registrant.session_id).first()
    assert updated_registrant.registration_value.get('addr') == '707 Vermont St'
    assert 'validated_addresses' in updated_registrant.registration_value
    assert updated_registrant.registration_value['validated_addresses']['current_address']['state'] == 'KS'

def test_vr_3_single_invalid_address(app, db_session, client):
    """
    An existing user provides an invalid address, but no previous address or mailing address. Should still redirect.
    """

    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {
        'addr': "123 Fake St",
        'city': "FakeTown",
        'state': "NA",
        'zip': '00000'
    }

    response = client.post('/vr/address', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/vr/party' in redirect_data) == True
    updated_registrant = db_session.query(Registrant).filter_by(session_id = registrant.session_id).first()
    assert updated_registrant.registration_value.get('addr') == '123 Fake St'
    assert 'validated_addresses' in updated_registrant.registration_value
    assert updated_registrant.registration_value['validated_addresses'] == False


def test_vr_3_with_prev_address(app, db_session, client):
    """
    An existing user provides a valid address and valid prev address
    """
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {
        'addr': "707 Vermont St",
        'unit': "Room A",
        'city': "Lawrence",
        'state': "KANSAS",
        'zip': '66044',
        'has_prev_addr': True,
        'prev_addr': "707 Vermont St",
        'prev_unit': "Room B",
        'prev_city': "Lawrence",
        'prev_state': "KANSAS",
        'prev_zip': '66044',
    }

    response = client.post('/vr/address', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/vr/party' in redirect_data) == True

    updated_registrant = db_session.query(Registrant).filter_by(session_id = registrant.session_id).first()
    assert updated_registrant.registration_value.get('addr') == '707 Vermont St'
    assert 'validated_addresses' in updated_registrant.registration_value
    assert updated_registrant.registration_value['validated_addresses']['current_address']['state'] == 'KS'
    assert updated_registrant.registration_value['validated_addresses']['prev_addr']['unit'] == 'RM B'

def test_vr_3_with_invalid_prev_address(app, db_session, client):
    """
    An existing user provides a valid address and invalid prev address
    """
    registrant = create_registrant(db_session)
    with client.session_transaction() as http_session:
        http_session['session_id'] = str(registrant.session_id)

    form_payload = {
        'addr': "707 Vermont St",
        'unit': "Room A",
        'city': "Lawrence",
        'state': "KANSAS",
        'zip': '66044',
        'has_prev_addr': True,
        'prev_addr': "123 Fake St",
        'prev_city': "FakeTown",
        'prev_state': "NA",
        'prev_zip': '00000'
    }

    response = client.post('/vr/address', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/vr/party' in redirect_data) == True
    updated_registrant = db_session.query(Registrant).filter_by(session_id = registrant.session_id).first()
    assert updated_registrant.registration_value.get('addr') == '707 Vermont St'
    assert 'validated_addresses' in updated_registrant.registration_value
    assert updated_registrant.registration_value['validated_addresses']['current_address']['state'] == 'KS'
    assert ('error' in updated_registrant.registration_value['validated_addresses']['prev_addr'])



def test_vr_3_with_mail_address(app, db_session, client):
     """
     An existing user provides a valid address and valid prev address
     """
     registrant = create_registrant(db_session)
     with client.session_transaction() as http_session:
         http_session['session_id'] = str(registrant.session_id)

     form_payload = {
         'addr': "707 Vermont St",
         'unit': "Room A",
         'city': "Lawrence",
         'state': "KANSAS",
         'zip': '66044',
         'has_mail_addr': True,
         'mail_addr': "707 Vermont St",
         'mail_unit': "Room B",
         'mail_city': "Lawrence",
         'mail_state': "KANSAS",
         'mail_zip': '66044',
     }

     response = client.post('/vr/address', data=form_payload, follow_redirects=False)
     redirect_data = response.data.decode()
     assert response.status_code == 302
     assert ('/vr/party' in redirect_data) == True

     updated_registrant = db_session.query(Registrant).filter_by(session_id = registrant.session_id).first()
     assert updated_registrant.registration_value.get('addr') == '707 Vermont St'
     assert 'validated_addresses' in updated_registrant.registration_value
     assert updated_registrant.registration_value['validated_addresses']['current_address']['state'] == 'KS'
     assert updated_registrant.registration_value['validated_addresses']['mail_addr']['unit'] == 'RM B'
