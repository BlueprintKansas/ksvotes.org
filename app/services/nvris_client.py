from flask import g, current_app
from app.main.VR.example_form import signature_img_string
import os
import requests
import json

class NVRISClient():

    def __init__(self, registrant):
        self.registrant = registrant
        self.lang = g.get('lang_code', current_app.config['BABEL_DEFAULT_LOCALE'])
        if self.lang == None:
            self.lang = registrant.lang or 'en' 
        self.nvris_url = os.getenv('NVRIS_URL')

    def get_vr_form(self):
        if self.nvris_url == 'TESTING': # magic URL for testing mode
            return signature_img_string

        url = self.nvris_url + '/vr/' + self.lang
        current_app.logger.info("%s NVRIS request to %s" %(self.registrant.session_id, url))
        payload = self.marshall_vr_payload()

        # remove the signature from payload if null because NVRIS will balk
        if not payload['signature']:
            payload.pop('signature')

        #print("payload: %s" %(payload)) # debug only -- no PII in logs
        try:
            resp = requests.post(url, json=payload)
            resp_payload = resp.json()
        except json.JSONDecodeError as e:
            current_app.logger.error("NVRIS responded with bad JSON: %s" %(e))
            return None
        return resp_payload['img']

    def marshall_vr_payload(self):
        r = self.registrant
        return {
            "00_citizen_yes": True if r.is_citizen else False,
            "00_citizen_no": False if r.is_citizen else True,
            "00_eighteenPlus_yes": True if r.is_eighteen else False,
            "00_eighteenPlus_no": False if r.is_eighteen else True,
            "01_prefix_mr": True if r.try_value('prefix') == 'mr' else False,
            "01_prefix_mrs": True if r.try_value('prefix') == 'mrs' else False,
            "01_prefix_miss": True if r.try_value('prefix') == 'miss' else False,
            "01_prefix_ms": True if r.try_value('prefix') == 'ms' else False,
            "01_suffix_jr": True if r.try_value('suffix') == 'jr' else False,
            "01_suffix_sr": True if r.try_value('suffix') == 'sr' else False,
            "01_suffix_ii": True if r.try_value('suffix') == 'ii' else False,
            "01_suffix_iii": True if r.try_value('suffix') == 'iii' else False,
            "01_suffix_iv": True if r.try_value('suffix') == 'iv' else False,
            "01_firstName": r.try_value('name_first'),
            "01_lastName": r.try_value('name_last'),
            "01_middleName": r.try_value('name_middle'),
            "02_homeAddress": r.try_value('addr'),
            "02_aptLot": r.try_value('unit'),
            "02_cityTown": r.try_value('city'),
            "02_state": r.try_value('state'),
            "02_zipCode": r.try_value('zip'),
            "03_mailAddress": r.try_value('mail_addr'),
            "03_cityTown": r.try_value('mail_city'),
            "03_state": r.try_value('mail_state'),
            "03_zipCode": r.try_value('mail_zip'),
            "04_dob": r.try_value('dob'),
            "05_telephone": r.try_value('phone'),
            "06_idNumber": r.try_value('id_number'),
            "07_party": r.party,
            "08_raceEthnic": '',
            "09_month": r.signed_at.strftime('%m'),
            "09_day": r.signed_at.strftime('%d'),
            "09_year": r.signed_at.strftime('%Y'),
            "A_prefix_mr": True if r.try_value('prev_prefix') == 'mr' else False,
            "A_prefix_mrs": True if r.try_value('prev_prefix') == 'mrs' else False,
            "A_prefix_miss": True if r.try_value('prev_prefix') == 'miss' else False,
            "A_prefix_ms": True if r.try_value('prev_prefix') == 'ms' else False,
            "A_suffix_jr": True if r.try_value('prev_suffix') == 'jr' else False,
            "A_suffix_sr": True if r.try_value('prev_suffix') == 'sr' else False,
            "A_suffix_ii": True if r.try_value('prev_suffix') == 'ii' else False,
            "A_suffix_iii": True if r.try_value('prev_suffix') == 'iii' else False,
            "A_suffix_iv": True if r.try_value('prev_suffix') == 'iv' else False,
            "A_firstName": r.try_value('prev_name_first'),
            "A_lastName": r.try_value('prev_name_last'),
            "A_middleName": r.try_value('prev_name_middle'),
            "B_homeAddress": r.try_value('prev_addr'),
            "B_aptLot": r.try_value('prev_unit'),
            "B_cityTown": r.try_value('prev_city'),
            "B_state": r.try_value('prev_state'),
            "B_zipCode": r.try_value('prev_zip'),
            "D_helper": r.try_value('helper'),
            "signature": r.try_value('signature_string', None),
        }
