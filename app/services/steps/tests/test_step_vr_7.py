from app.models import *
from app.services.steps import Step_VR_7

def test_step_vr7_is_complete_false(app, db_session, client):
    form_payload = {}
    step = Step_VR_7(form_payload)
    assert step.run() == False
    assert step.is_complete == False
    assert step.next_step == None


def test_step_vr7_is_complete_true(app, db_session, client):
    form_payload = {
        "affirmation": True
    }
    step = Step_VR_7(form_payload)
    assert step.run() == True
    assert step.is_complete == True
    assert step.next_step == 'Step_VR_8'
