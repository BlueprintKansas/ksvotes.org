from app.models import *
from app.services.steps import Step_VR_5

def test_step_vr5_is_complete_false(app, db_session, client):
    """
        Verify that this registrant is not ready to move on to the next step.

    """
    form_payload = {}
    step = Step_VR_5(form_payload)
    assert step.run() == False
    assert step.is_complete == False
    assert step.next_step == None


def test_step_vr5_is_complete_true(app, db_session, client):
    """
        Verify that this registrant is not ready to move on to the next step and next step is VR 6.

    """
    form_payload = {
        "identification": "nnnnnnn"
    }
    step = Step_VR_5(form_payload)
    assert step.run() == True
    assert step.is_complete == True
    assert step.next_step == 'Step_VR_6'
