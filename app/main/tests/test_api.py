import datetime
import uuid
from app.models import Registrant


def test_api_total_processed(app, db_session, client):
    # We should be empty at first
    response = client.get('/api/total-processed/')
    assert response.status_code == 200
    data = response.get_json()
    assert data["registrations"] == 0
    assert data["advanced_ballots"] == 0

    now = datetime.datetime.utcnow()

    new_registrant = Registrant(
        lang='en',
        county="Johnson",
        vr_completed_at=now
    )
    db_session.add(new_registrant)
    db_session.commit()

    # We should have a single registrant now
    response = client.get('/api/total-processed/')
    assert response.status_code == 200
    data = response.get_json()
    assert data["registrations"] == 1
    assert data["advanced_ballots"] == 0

    second_registrant = Registrant(
        lang='en',
        county="Johnson",
        ab_completed_at=now,
        session_id=uuid.uuid4(),
    )
    db_session.add(second_registrant)
    db_session.commit()

    # We should have a second registrant now
    response = client.get('/api/total-processed/')
    assert response.status_code == 200
    data = response.get_json()
    assert data["registrations"] == 1
    assert data["advanced_ballots"] == 1
