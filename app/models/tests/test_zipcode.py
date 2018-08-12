from app.models import *

def test_zipcode(app, db_session, client):
    z = ZIPCode.find_by_zip5('66044')
    assert len(z.counties) == 3

    assert ZIPCode.guess_county('66044') == 'Douglas'

