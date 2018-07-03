from app.models import *
from app.services.steps import Step_AB_3

def test_step_ab3_is_complete_false_with_missing_arguments(app, db_session, client):
    form_payload = {}
    step = Step_AB_3(form_payload)
    assert step.run() == False
    assert step.is_complete == False
    assert step.next_step == None


def test_step_ab3_is_complete_true_with_one_address(app, db_session, client):
    form_payload = {
        'addr': "707 Vermont St",
        'unit': "Room A",
        'city': "Lawrence",
        'state': "KANSAS",
        'zip': '66044'
    }
    step = Step_AB_3(form_payload)
    step.run()
    assert step.run() == True
    assert step.is_complete == True
    assert 'current_address' in step.validated_addresses
    assert step.validated_addresses['current_address']['state'] == 'KS'
    assert step.addr_lookup_complete == True
    assert step.next_step == 'Step_AB_5'

def test_step_ab3_is_complete_false_with_bad_address(app, db_session, client):
    form_payload = {
        'addr': "123 Fake St",
        'city': "Fake",
        'state': "NA",
        'zip': '66044',
    }
    step = Step_AB_3(form_payload)
    step.run()
    assert step.validated_addresses == False
    assert step.is_complete == True
    assert step.addr_lookup_complete == True


def test_step_ab3_with_mail_addr(app, db_session, client):
    form_payload3 = {
        'addr': "707 Vermont St",
        'unit': "Room A",
        'city': "Lawrence",
        'state': "KANSAS",
        'zip': '66044',
        'has_mail_addr': True,
        'mail_addr': "707 Vermont St",
        'mail_unit': "Room C",
        'mail_city': "Lawrence",
        'mail_state': "KANSAS",
        'mail_zip': '66044',
    }
    step = Step_AB_3(form_payload3)
    step.run()
    assert step.is_complete == True
    assert step.next_step == 'Step_AB_5'
    assert 'current_address' in step.validated_addresses
    assert step.validated_addresses['current_address']['unit'] == 'RM A'
    assert step.addr_lookup_complete == True
    assert 'mail_addr' in step.validated_addresses
    assert step.validated_addresses['mail_addr']['unit'] == 'RM C'
