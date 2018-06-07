from app.models import *
from app.main.forms import FormStep0

#NOTE session in the functions is a bit of a misnomer it is really the db session not the client session

def test_create_new_session_step_0(app, session, client):
    with client.session_transaction() as sess:
        assert sess.get('session_id') == None
    response = client.post('/', data=dict(
        name_first="foo",
        name_last="bar",
        dob="01/01/2000",
        county="Douglas",
        email="foo@example.com",
    ), follow_redirects=False)

    assert response.status_code == 302
    #this will change to ab router

    with client.session_transaction() as sess:
        assert sess.get('session_id') != None

def test_update_name_step_0_session_exists_already(app,session,client):
    #will fail
    # if active session exists update step 0 records
    data = {
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
        registration_value = data,
    )
    session.add(new_registrant)
    session.commit()

    with client.session_transaction() as sess:
        sess['session_id'] = str(new_registrant.session_id)
        current_registrant = Registrant.query.filter(Registrant.session_id == sess.get('session_id')).first()
        assert current_registrant.registration_value.get('name_first') == 'foo'

        name_update = {
            "name_first": "baz",
            "county": "Douglas"
        }
        current_registrant.update(name_update)
        session.commit()

        current_registrant_updated = Registrant.query.filter(Registrant.session_id == sess.get('session_id')).first()
        assert current_registrant_updated.registration_value.get('name_first') == 'baz'
        assert current_registrant_updated.id == current_registrant.id
