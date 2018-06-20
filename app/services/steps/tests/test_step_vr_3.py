from app.models import *
from app.services.steps import Step_VR_3

def test_step_vr3_is_complete_false_with_missing_arguments(app, db_session, client):
    """
        Verify that this registrant is not ready to move on to vr3 next step.
    """
    form_payload = {}
    step = Step_VR_3(form_payload)
    assert step.run() == False
    assert step.is_complete == False
    assert step.next_step == None


def test_step_vr3_is_complete_true_with_one_address(app, db_session, client):
    """
        Verify that this registrant is ready to move on to the next step and next step is VR 4.
    """
    form_payload = {
        'addr': "707 Vermont St",
        'unit': "Room A",
        'city': "Lawrence",
        'state': "KANSAS",
        'zip': '66044'
    }
    step = Step_VR_3(form_payload)
    step.run()
    assert step.run() == True
    assert step.is_complete == True
    assert 'current_address' in step.validated_addresses
    assert step.validated_addresses['current_address']['state'] == 'KS'
    assert step.addr_lookup_complete == True
    assert step.next_step == 'Step_VR_4'

def test_step_vr3_is_complete_false_with_bad_address(app, db_session, client):
    """
        Verify that this registrant is not ready to move on to the next step and next step is VR 4.
    """
    form_payload = {
        'addr': "123 Fake St",
        'city': "Fake",
        'state': "NA",
        'zip': '66044',
    }
    step = Step_VR_3(form_payload)
    step.run()
    assert step.validated_addresses == False
    assert step.is_complete == True
    assert step.addr_lookup_complete == True

def test_step_vr3_with_prev_address(app, db_session, client):
    form_payload = {
        'addr': "707 Vermont St",
        'unit': "Room A",
        'city': "Lawrence",
        'state': "KANSAS",
        'zip': '66044',
        'has_prev_addr': True,
        'prev_addr': "707 Vermont St",
        'prev_unit': "Room B",
        'prev_city': "Lawrence",
        'prev_state': "KANSAS",
        'prev_zip': '66044',
    }
    step = Step_VR_3(form_payload)
    step.run()
    assert step.is_complete == True
    assert step.next_step == 'Step_VR_4'
    assert 'current_address' in step.validated_addresses
    assert step.validated_addresses['current_address']['unit'] == 'RM A'
    assert 'prev_addr' in step.validated_addresses
    assert step.validated_addresses['prev_addr']['unit'] == 'RM B'
    assert step.addr_lookup_complete == True


def test_step_vr3_with_bad_prev_address(app, db_session, client):
    form_payload = {
        'addr': "707 Vermont St",
        'unit': "Room A",
        'city': "Lawrence",
        'state': "KANSAS",
        'zip': '66044',
        'has_prev_addr': True,
        'prev_addr': "foo",
        'prev_unit': "bar",
        'prev_city': "baz",
        'prev_state': "nitro",
        'prev_zip': '',
    }
    step = Step_VR_3(form_payload)
    step.run()
    assert step.is_complete == True
    assert step.next_step == 'Step_VR_4'
    assert 'current_address' in step.validated_addresses
    assert step.validated_addresses['current_address']['unit'] == 'RM A'
    assert 'prev_addr' in step.validated_addresses
    assert 'error' in step.validated_addresses['prev_addr']


def test_step_vr3_with_prev_address_and_mail_addr(app, db_session, client):
     form_payload3 = {
         'addr': "707 Vermont St",
         'unit': "Room A",
         'city': "Lawrence",
         'state': "KANSAS",
         'zip': '66044',
         'has_prev_addr': True,
         'prev_addr': "707 Vermont St",
         'prev_unit': "Room B",
         'prev_city': "Lawrence",
         'prev_state': "KANSAS",
         'prev_zip': '66044',
         'has_mail_addr': True,
         'mail_addr': "707 Vermont St",
         'mail_unit': "Room C",
         'mail_city': "Lawrence",
         'mail_state': "KANSAS",
         'mail_zip': '66044',
     }
     step = Step_VR_3(form_payload3)
     step.run()
     assert step.is_complete == True
     assert step.next_step == 'Step_VR_4'
     assert 'current_address' in step.validated_addresses
     assert step.validated_addresses['current_address']['unit'] == 'RM A'
     assert 'prev_addr' in step.validated_addresses
     assert step.validated_addresses['prev_addr']['unit'] == 'RM B'
     assert step.addr_lookup_complete == True
     assert 'mail_addr' in step.validated_addresses
     assert step.validated_addresses['mail_addr']['unit'] == 'RM C'
