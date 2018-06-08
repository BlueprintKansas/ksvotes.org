from app.models import *
from app.services.steps import Step_0

def test_step_0_is_complete_false(app, session, client):
    """
        Verify that this registrant is not ready to move on to the next step.

    """
    form_payload = {
        "name_first": "foo"
    }
    step = Step_0(form_payload)
    assert step.validate() == False
    assert step.is_complete == False

def test_step_0_is_complete_true_and_none_registered(app,session,client):
    """
        Verify that all of the information for step 0 is saved to the registrant.
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
    assert step.validate() == True
    assert step.is_complete == True
    # assert step.next_step == '/vr/citizenship'

def test_step_0_is_complete_true_and_already_registered(app,session,client):
    form_payload = {
        "name_first": "Jake",
        "name_last": "Lowen",
        "dob":"02/07/1979",
        "email":"foo@example.com",
        "county": "Douglas"
    }
    step = Step_0(form_payload)
    assert step.validate() == True
    assert step.is_complete == True
    # assert step.next_step == '/change-or-apply'
