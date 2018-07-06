from app.models import *
from app.services.steps import Step_AB_5

def test_step_ab5_is_complete_false(app, db_session, client):
    form_payload = {}
    step = Step_AB_5(form_payload)
    assert step.run() == False
    assert step.is_complete == False
    assert step.next_step == None


def test_step_ab5_is_complete_true(app, db_session, client):
    form_payload = {
        "identification": "nnnnnnn"
    }
    step = Step_AB_5(form_payload)
    assert step.run() == True
    assert step.is_complete == True
    assert step.next_step == 'Step_AB_6'
