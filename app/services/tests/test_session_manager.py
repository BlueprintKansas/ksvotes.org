from app.models import Registrant
from app.services import SessionManager
from app.services.steps import Step_0, Step_VR_1

def create_registrant(db_session):
    registrant = Registrant(
        registration_value={
            "name_first": "foo",
        },
    )
    db_session.add(registrant)
    db_session.commit()
    return registrant

def test_non_previous_step_non_complete_step(app, db_session, client):
    """
    A non complete step should return the current steps endpoint
    """
    registrant = create_registrant(db_session)
    step = Step_0()
    session_manager = SessionManager(registrant, step)
    assert session_manager.get_redirect_url() == step.endpoint

def test_no_previous_step_is_complete(app,db_session,client):
    """
    A complete step should return the next steps endpoint
    """
    registrant = create_registrant(db_session)
    step = Step_0()
    #mock step actions
    step.is_complete = True
    step.next_step = 'Step_VR_1'

    session_manager = SessionManager(registrant, step)
    assert session_manager.get_redirect_url() == '/vr/citizenship'


def test_registrant_doesnt_have_values(app, db_session, client):
    """
    A registrant should be redirected to previous step if missing values of that step
    """
    registrant = create_registrant(db_session)
    form_payload = {'is_citizen': True}
    step = Step_VR_1(form_payload)
    step.run()

    session_manager = SessionManager(registrant, step)
    assert session_manager.get_redirect_url() == '/'

def test_completion_logic(app, db_session, client):
    registrant = create_registrant(db_session)
    step = Step_0()
    session_manager = SessionManager(registrant, step)
    assert session_manager.vr_completed() == False
    assert session_manager.ab_completed() == False

    registrant.last_completed_step = 7
    registrant.update({'vr_form':'foobar'})
    registrant.save(db_session)
    session_manager = SessionManager(registrant, step)
    assert session_manager.vr_completed() == True
    assert session_manager.ab_completed() == False

    registrant.update({'ab_forms':'foobar'})
    registrant.save(db_session)
    session_manager = SessionManager(registrant, step)
    assert session_manager.vr_completed() == True
    assert session_manager.ab_completed() == True
