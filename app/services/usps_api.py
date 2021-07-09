import os
from pyusps import address_information
from collections import OrderedDict
from flask import current_app

class USPS_API():
    def __init__(self, address_payload = None):
        self.address_payload = address_payload
        self.usps_id = os.getenv('USPS_USER_ID')
        self.address_order = ['current_address']

    def marshall_single_address(self, address):
        """
        Convert a single address from pyusps into a dictionary with the correct k,vs or an en error
        """
        marshalled_address = {}
        if isinstance(address, OrderedDict):
            for k,v in address.items():
                if k == 'address_extended':
                    marshalled_address['unit'] = v
                else:
                    marshalled_address[k] = v
        elif isinstance(address, ValueError):
            marshalled_address['error'] = "There was an issue validating your address."

        return marshalled_address

    def marshall_address_results(self, validated_addresses):
        """
        Take a pyusps result and determine if it is a single address or list of addresses, then marshal each address and return the full marshalled dictionary.
        """
        marshalled_addresses = {}
        if isinstance(validated_addresses, OrderedDict):
            marshalled_addresses['current_address'] = self.marshall_single_address(validated_addresses)
        elif isinstance(validated_addresses, list):
            for count, address in enumerate(validated_addresses):
                marshalled_addresses[self.address_order[count]] = self.marshall_single_address(address)
        else:
            raise "Invalid addresses, cannot marshall"

        return marshalled_addresses


    def validate_addresses(self):
        """
        Return values of usps lookup.  Keep track of order of addresses if multiple provided.
        """
        addresses = []

        # always expect the current address
        addresses.append(dict([
            ('address', self.address_payload.get('addr', '')),
            ('city', self.address_payload.get('city', '')),
            ('state', self.address_payload.get('state', '')),
            ('zip_code', self.address_payload.get('zip','')),
            ('address_extended', self.address_payload.get('unit',''))
        ]))

        #construct additional addresses for request and update address_order
        if self.address_payload.get('has_prev_addr', None) == True:
            self.address_order.append('prev_addr')
            addresses.append(dict([
                ('address', self.address_payload.get('prev_addr', '')),
                ('city', self.address_payload.get('prev_city', '')),
                ('state', self.address_payload.get('prev_state', '')),
                ('zip_code', self.address_payload.get('prev_zip', '')),
                ('address_extended', self.address_payload.get('prev_unit', ''))
            ]))

        if self.address_payload.get('has_mail_addr', None) == True:
            self.address_order.append('mail_addr')
            addresses.append(dict([
                ('address', self.address_payload.get('mail_addr', '')),
                ('city', self.address_payload.get('mail_city', '')),
                ('state', self.address_payload.get('mail_state', '')),
                ('zip_code', self.address_payload.get('mail_zip', '')),
                ('address_extended', self.address_payload.get('mail_unit', ''))
            ]))

        current_app.logger.debug("Trying USPS address lookup")
        results = self.verify_with_usps(addresses)
        current_app.logger.debug("USPS API returned {}".format(results))
        if results:
            return self.marshall_address_results(results)
        else:
            return False

    def verify_with_usps(self, addresses):
        ### Needs to be in a try block for the usps verify method to not raise an error
        try:
            return address_information.verify(self.usps_id, *addresses)
        except:
            return False
