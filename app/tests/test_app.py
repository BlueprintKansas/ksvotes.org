def test_app(app, session, client):
    assert app.testing == True

def test_homepage(app, session, client):
    response = client.get('/')
    assert response.status_code == 200
