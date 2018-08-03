def test_app(app, db_session, client):
    assert app.testing == True

def test_homepage(app, db_session, client):
    response = client.get('/')
    assert response.status_code == 200

def test_404(app, db_session, client):
    response = client.get('/asdfasdfadcasdcmasdocasdf/')
    assert response.status_code == 404

    response = client.get('/es/foo/bar')
    assert response.status_code == 404

# helpers
from app.main.helpers import *

def test_helpers(app, db_session, client):
    election_date = parse_election_date('General')
    assert election_date == None

