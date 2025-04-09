import g
import sys, traceback
import logging
import copy
from flask import Flask, request, make_response
from flask_restful import reqparse, Api, Resource

# Import BIOS settings template function
from .templates.bios_settings import get_Bios_Settings_instance

# Dictionary to store BIOS settings for multiple systems
bios_setting = {}  
INTERNAL_ERROR = 500

# BIOS Settings Singleton API
class BiosSettingsAPI(Resource):

    def __init__(self, **kwargs):
        logging.info('BiosSettingsAPI init called')
        self.rb = kwargs.get('rb', '')  # Get the Redfish base URL

    # HTTP GET - Retrieve BIOS settings for a specific system
    def get(self, ident):
        logging.info(f'BiosSettingsAPI GET called for system {ident}')
        try:
            global bios_setting
            # Check if the system already exists, if not, create it
            if ident not in bios_setting:
                bios_setting[ident] = get_Bios_Settings_instance({'rb': self.rb, 'id': ident})
            
            return bios_setting[ident], 200
        except Exception:
            traceback.print_exc()
            return INTERNAL_ERROR

    # HTTP PATCH - Update BIOS settings for a specific system
    def patch(self, ident):
        logging.info(f'BiosSettingsAPI PATCH called for system {ident}')
        try:
            global bios_setting
            if not request.json:
                return "Invalid input, expected JSON", 400

            # Ensure the system exists
            if ident not in bios_setting:
                bios_setting[ident] = get_Bios_Settings_instance({'rb': self.rb, 'id': ident})

            # Update only the specified attributes
            for key, value in request.json.items():
                if key in bios_setting[ident]['Attributes']:
                    bios_setting[ident]['Attributes'][key] = value
                else:
                    return f"Invalid BIOS attribute: {key}", 400

            return bios_setting[ident], 200
        except Exception:
            traceback.print_exc()
            return INTERNAL_ERROR
        
def get_bios_settings(ident):
    if ident not in bios_setting:
        bios_setting[ident] = get_Bios_Settings_instance({'rb': '/redfish/v1/', 'id': ident})
    return bios_setting[ident]