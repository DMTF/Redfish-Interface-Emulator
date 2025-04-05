import g
import sys, traceback
import logging
import copy
from flask import Flask, request, make_response
from flask_restful import reqparse, Api, Resource

# Resource and SubResource imports
from .templates.Bios import get_Bios_instance

config = {}
INTERNAL_ERROR = 500

# BIOS Singleton API
class BiosAPI(Resource):
    

    def __init__(self, **kwargs):
        logging.info('BiosAPI init called')
        self.rb = kwargs.get('rb', '')  # Get the Redfish base URL

    # HTTP GET
    def get(self, ident):  # Add 'ident' to capture the system ID from the URL
        logging.info(f'BiosAPI GET called for system {ident}')
        try:
            global bios_config
            # Pass the extracted 'ident' (system ID) to get_Bios_instance
            bios_config = get_Bios_instance({'rb': self.rb, 'id': ident})  
            return bios_config, 200
        except Exception:
            traceback.print_exc()
            return INTERNAL_ERROR