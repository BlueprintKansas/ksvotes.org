from app.models import *


def test_citizenship_not_checked_does_not_return_redirect(app, session, client):
    """
    An existing user tries to update their record, but does not select the citizen checkbox
    """
    form_payload = {}
    response = client.post('/vr/citizenship', data=form_payload, follow_redirects=False)
    assert response.status_code != 302

def test_citizenship_checked_returns_redirect(app,session,client):
    form_payload = {"citizen": True}
    response = client.post('/vr/citizenship', data=form_payload, follow_redirects=False)
    redirect_data = response.data.decode()
    assert response.status_code == 302
    assert ('/vr/name' in redirect_data) == True
