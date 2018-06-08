# from app.models import *
# from app.services.steps import Step_VR_1
#
# def test_step_vr1_is_complete_false(app, session, client):
#     """
#         Verify that this registrant is not ready to move on to the next step.
#
#     """
#     form_payload = {}
#     step = Step_VR_1(form_payload)
#     assert step.is_complete() == False
#
# def test_step_vr1_is_complete_true(app, session, client):
#     """
#         Verify that this registrant is not ready to move on to the next step.
#
#     """
#     form_payload = {
#         "citizen": True
#     }
#     step = Step_VR_1(form_payload)
#     assert step.is_complete() == True
#     assert step.next_step() == '/vr/name'
