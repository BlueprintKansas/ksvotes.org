# from app.models import *
# from app.services.steps import Step_VR_3
#
# def test_step_vr3_is_complete_false(app, session, client):
#     """
#         Verify that this registrant is not ready to move on to the next step.
#
#     """
#     form_payload = {}
#     step = Step_VR_3(form_payload)
#     assert step.is_complete() == False
#
# def test_step_vr3_with_fakeaddress(app,session,client):
#     form_payload = {
#         "addr": "123 Fake St",
#         "city": "Madeup",
#         "state": "KANSAS",
#         "zip": "99999"
#     }
#     step = Step_VR_3(form_payload)
#     assert step.is_complete() == False
#
# def test_step_vr3_is_complete_true(app, session, client):
#     """
#         Verify that this registrant is not ready to move on to the next step.
#
#     """
#     form_payload = {
#         "addr": "7223 Eby Dr",
#         "unit": "107",
#         "city": "Merriam",
#         "state": "KANSAS",
#         "zip": "66204"
#     }
#     step = Step_VR_3(form_payload)
#     assert step.is_complete() == True
#     assert step.next_step() == '/vr/party'
