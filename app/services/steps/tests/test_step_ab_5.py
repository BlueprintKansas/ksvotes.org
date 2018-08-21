from app.models import *
from app.services.steps import Step_AB_5

def test_step_ab5_is_complete_when_null(app, db_session, client):
    form_payload = {}
    step = Step_AB_5(form_payload)
    assert step.run() == True
    assert step.is_complete == True
    assert step.next_step == 'Step_AB_6'


def test_step_ab5_is_complete_when_valid_pattern(app, db_session, client):
    form_payload = {
        "ab_identification": "K00000000"
    }
    step = Step_AB_5(form_payload)
    assert step.run() == True
    assert step.is_complete == True
    assert step.next_step == 'Step_AB_6'

def test_step_ab5_is_incomplete_when_invalid_pattern(app, db_session, client):
    form_payload = {
        "ab_identification": "not valid"
    }
    step = Step_AB_5(form_payload)
    assert step.run() == False
    assert step.is_complete == False
    assert step.next_step == None
