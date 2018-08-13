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
        payload = self.marshall_payload('vr')

        #print("payload: %s" %(payload)) # debug only -- no PII in logs
        return self.fetch_nvris_img(url, payload)

    def get_ab_form(self, election):
        if self.nvris_url == 'TESTING': # magic URL for testing mode
            return signature_img_string

        if self.registrant.try_value('ab_permanent'):
            flavor = 'ksav2'
        else:
            flavor = 'ksav1'
    
        url = self.nvris_url + '/av/' + flavor

        current_app.logger.info("%s NVRIS request to %s" %(self.registrant.session_id, url))
        payload = self.marshall_payload(flavor, election=election)

        #print("payload: %s" %(payload)) # debug only -- no PII in logs
        return self.fetch_nvris_img(url, payload)

    def fetch_nvris_img(self, url, payload):
        try:
            resp = requests.post(url, json=payload)
            resp_payload = resp.json()
        except requests.exceptions.ConnectionError as e:
            current_app.logger.error("NVRIS did not respond: %s" %(e))
            return None
        except json.JSONDecodeError as e:
            current_app.logger.error("NVRIS responded with bad JSON: %s" %(e))
            return None

        if 'img' not in resp_payload:
            current_app.logger.error("NVRIS did not respond with img: %s" %(resp_payload))

        return resp_payload['img']

    def marshall_payload(self, flavor, **kwargs):
        if flavor == 'vr':
            payload = self.marshall_vr_payload()
        elif flavor == 'ksav1':
            payload = self.marshall_ksav1_payload(**kwargs)
        elif flavor == 'ksav2':
            payload = self.marshall_ksav2_payload()
        else:
            raise Exception("unknown payload flavor %s" %(flavor))

        # remove the signature from payload if null because NVRIS will balk
        if not payload['signature']:
            payload.pop('signature')

        return payload

    def parse_election_date(self, election):
        import re
        pattern = '(Primary|General) \((.+)\)'
        m = re.match(pattern, election)
        return m.group(2)

    def marshall_ksav1_payload(self, **kwargs):
        election = kwargs['election']
        r = self.registrant
        sig = r.try_value('signature_string', None)
        return {
            'state': 'Kansas', # TODO r.try_value('state'),
            'county_2': r.county, # TODO corresponds with 'state'
            'county_1': r.county, # TODO different?
            'id_number': r.try_value('ab_identification'),
            'last_name': r.try_value('name_last'),
            'first_name': r.try_value('name_first'),
            'middle_initial': r.middle_initial(),
            'dob': r.try_value('dob'),
            'residential_address': r.try_value('addr'),
            'residential_city': r.try_value('city'),
            'residential_state': r.try_value('state'),
            'residential_zip': r.try_value('zip'),
            'mailing_address': r.try_value('mail_addr'),
            'mailing_city': r.try_value('mail_city'),
            'mailing_state': r.try_value('mail_state'),
            'mailing_zip': r.try_value('mail_zip'),
            'election_date': self.parse_election_date(election),
            'signature': sig,
            'signature_date': r.signed_at.strftime('%m/%d/%Y') if sig else False,
            'phone_number': r.try_value('phone'),
            'democratic': True if r.party.lower() == 'democratic' else False,
            'republican': True if r.party.lower() == 'republican' else False,
        }

    def marshall_vr_payload(self):
        r = self.registrant
        sig = r.try_value('signature_string', None)
        return {
            "00_citizen_yes": True if r.is_citizen else False,
            "00_citizen_no": False if r.is_citizen else True,
            "00_eighteenPlus_yes": True if r.is_eighteen else False,
            #"00_eighteenPlus_no": False if r.is_eighteen else True,
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
            "06_idNumber": r.try_value('identification'),
            "07_party": r.party,
            "08_raceEthnic": '',
            "09_month": r.signed_at.strftime('%m') if sig else False,
            "09_day": r.signed_at.strftime('%d') if sig else False,
            "09_year": r.signed_at.strftime('%Y') if sig else False,
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
            "signature": sig,
        }
