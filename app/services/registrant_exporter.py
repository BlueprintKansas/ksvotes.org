import csv
import sys
from app.models import Registrant

class RegistrantExporter():

    def __init__(self, list_of_regs):
        self.list_of_regs = list_of_regs

    def export(self):
        # must iterate over all rows to create the header,
        # because not every row has all the same encrypted fields.

        unique_field_names = {}
        reg_dicts = []
        for r in self.list_of_regs:
            r_dict = dict(r.__dict__)
            reg_dicts.append(r_dict)
            for k, v in r.registration_value.items():
                if k == 'csrf_token':
                    continue
                unique_field_names['r_'+k] = True
                r_dict['r_'+k] = v

        fieldnames = list(Registrant.__table__.columns.keys()) + list(unique_field_names.keys())
        fieldnames.remove('registration') # no need for encrypted blob

        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        for r_dict in reg_dicts:
            r_dict.pop('registration', None)
            r_dict.pop('_sa_instance_state', None)
            writer.writerow(r_dict)
