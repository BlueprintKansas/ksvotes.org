from app.models import *

def test_ref_post_external_org(app, db_session, client):
	ref_payload = {
		'name_first': 'Foo',
		'name_last': 'Bar',
		'email': 'foobar@example.com',
	}
	response = client.post('/ref?ref=someorg', data=ref_payload, follow_redirects=False)
	with client.session_transaction() as http_session:
		sid = http_session.get('session_id')
		registrant = Registrant.lookup_by_session_id(sid)

		assert response.status_code == 302
		assert sid != None
		assert registrant.try_value('name_first') == 'Foo'
		assert registrant.ref == 'someorg'

def test_ref_get_fails(app, db_session, client):
	assert client.get('/ref/?ref=foo').status_code == 404
	assert client.post('/ref/').status_code == 404
