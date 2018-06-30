from app.models import *
from app.services.steps import Step_0

def test_step_0_is_complete_false(app, db_session, client):
    """
        Verify that this registrant is not ready to move on to the next step.

    """
    form_payload = {
        "name_first": "foo"
    }
    step = Step_0(form_payload)
    assert step.run() == False
    assert step.is_complete == False
    assert step.next_step == None

def test_step_0_is_complete_true_and_none_registered(app,db_session,client):
    """
        Verify that next step is VR Step 1
    """
    form_payload = {
        "name_first": "foo",
        "name_last": "bar",
        "dob":"01/01/2000",
        "email":"foo@example.com",
        "county": "Douglas"
    }
    step = Step_0(form_payload)
    assert step.run() == True
    assert step.is_complete == True
    assert step.next_step == 'Step_VR_1'

def test_step_0_is_complete_true_and_already_registered(app,db_session,client):
    """
        Verify that next step is AB 1
    """
    form_payload = {
        "name_first": "Kris",
        "name_last": "Kobach",
        "dob":"03/26/1966",
        "email":"foo@example.com",
        "county": "Douglas"
    }
    step = Step_0(form_payload)
    assert step.run() == True
    assert step.is_complete == True
    assert step.next_step == 'Step_1'
