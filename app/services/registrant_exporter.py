import csv
import sys
from app.models import Registrant

class RegistrantExporter():

    def __init__(self, list_of_regs):
        self.list_of_regs = list_of_regs

    def export(self):
        # use the first item to create our header
        r1 = self.list_of_regs[0]
        fieldnames = list(dict(r1.__dict__).keys())

        fieldnames.remove('_sa_instance_state') # internal key
        fieldnames.remove('registration') # no need for encrypted blob

        # append all the encrypted key names
        # we use the r_ prefix just to namespace and avoid any collisions.
        for k in r1.registration_value.keys():
            if k == 'csrf_token':
                continue
            fieldnames.append('r_'+k)

        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        
        for r in self.list_of_regs:
            r_dict = dict(r.__dict__)
            for k, v in r.registration_value.items():
                if k == 'csrf_token':
                    continue
                r_dict['r_'+k] = v

            r_dict.pop('registration', None)
            r_dict.pop('_sa_instance_state', None)

            writer.writerow(r_dict)
