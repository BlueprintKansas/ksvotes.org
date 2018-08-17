from app.models import *
from app.services.steps import Step_AB_1
from flask import g
from datetime import datetime

def test_step_ab1_is_complete_false(app, db_session, client):
    form_payload = {}
    g.registrant = Registrant()
    step = Step_AB_1(form_payload)
    assert step.run() == False
    assert step.is_complete == False
    assert step.next_step == None

def test_step_ab1_is_complete_true(app, db_session, client):
    form_payload = {
        "elections": "General (November 6, 2018)"
    }
    g.registrant = Registrant()
    step = Step_AB_1(form_payload)
    assert step.run() == True
    assert step.is_complete == True
    assert step.next_step == 'Step_AB_3'

def test_step_ab1_is_complete_with_registrant_skips_address(app, db_session, client):
    form_payload = {
        "elections": "General (November 6, 2018)"
    }
    g.registrant = Registrant(vr_completed_at=datetime.utcnow())
    step = Step_AB_1(form_payload)
    assert step.run() == True
    assert step.is_complete == True
    assert step.next_step == 'Step_AB_5'

