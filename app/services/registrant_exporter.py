import csv
import sys
from app.models import Registrant

class RegistrantExporter():

    def __init__(self, list_of_regs):
        self.list_of_regs = list_of_regs

    def export(self):
        skip_fields = [
            'csrf_token',
            'identification',
            'ab_identification',
            'vr_form',
            'ab_forms',
            'signature_string'
        ]
        fieldnames = [
            "id",
            "created_at",
            "updated_at",
            "vr_completed_at",
            "ab_completed_at",
            "redacted_at",
            "ab_permanent",
            "session_id",
            "ref",
            "is_citizen",
            "is_eighteen",
            "dob_year",
            "party",
            "county",
            "lang",
            "signed_at",
            "reg_lookup_complete",
            "addr_lookup_complete",
            "reg_found",
            "identification_found",
            "ab_identification_found",
            "r_ref",
            "r_name_first",
            "r_name_last",
            "r_dob",
            "r_county",
            "r_email",
            "r_phone",
            "r_sos_reg",
            "r_skip_sos",
            "r_prefix",
            "r_name_middle",
            "r_suffix",
            "r_has_prev_name",
            "r_prev_prefix",
            "r_prev_name_first",
            "r_prev_name_middle",
            "r_prev_name_last",
            "r_prev_suffix",
            "r_addr",
            "r_unit",
            "r_city",
            "r_state",
            "r_zip",
            "r_has_prev_addr",
            "r_prev_addr",
            "r_prev_unit",
            "r_prev_city",
            "r_prev_state",
            "r_prev_zip",
            "r_has_mail_addr",
            "r_mail_addr",
            "r_mail_unit",
            "r_mail_city",
            "r_mail_state",
            "r_mail_zip",
            "r_validated_addresses",
            "r_affirmation",
            "r_vr_form_message_id",
            "r_recaptcha",
            "r_elections",
            "r_sos_failure",
            "r_perm_reason",
            "r_ab_forms_message_id",
        ]

        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        for r in self.list_of_regs:
            r_dict = dict(r.__dict__)
            for k, v in r.registration_value.items():
                if k in skip_fields:
                    continue
                r_dict['r_'+k] = v

            r_dict.pop('registration', None)
            r_dict.pop('_sa_instance_state', None)
            writer.writerow(r_dict)

