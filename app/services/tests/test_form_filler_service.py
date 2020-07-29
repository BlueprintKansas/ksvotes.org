import json
import re
import base64
import pprint
from app.services import FormFillerService

def test_vr_en_form(app, db_session, client):
  payload_file = 'app/services/tests/test-vr-en-payload.json'
  with open(payload_file) as payload_f:
    payload = json.load(payload_f)

    ffs = FormFillerService(payload=payload, form_name='/vr/en')
    img = ffs.as_image()
    app.logger.info("got image:{}".format(img))
    matches = re.fullmatch(r"(data:image\/(.+?);base64),(.+)", img, re.I)

    assert matches.group(1) == 'data:image/png;base64'
    assert matches.group(2) == 'png'
    assert base64.b64decode(matches.group(3))
