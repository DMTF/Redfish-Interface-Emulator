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

ALLOWED_BIOS_ATTRIBUTES = {
    "AdminPhone": str,
    "BootMode": str,
    "EmbeddedSata": str,
    "NicBoot1": str,
    "NicBoot2": str,
    "PowerProfile": str,
    "ProcCoreDisable": int,
    "ProcHyperthreading": ["Enabled", "Disabled"],
    "ProcTurboMode": ["Enabled", "Disabled"],
    "UsbControl": str
}

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
            return {"error": "Internal server error"}, INTERNAL_ERROR

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
                if key not in ALLOWED_BIOS_ATTRIBUTES:
                    return {"error": f"Invalid BIOS attribute: {key}"}, 400
                allowed_type = ALLOWED_BIOS_ATTRIBUTES[key]

                if isinstance(allowed_type, list):
                    if value not in allowed_type:
                        return {"error": f"Invalid value for {key}. Must be one of {allowed_type}"}, 400
                elif not isinstance(value, allowed_type):
                    return {"error": f"Invalid type for {key}. Expected {allowed_type.__name__}"}, 400
                bios_setting[ident]['Attributes'][key] = value
            return bios_setting[ident], 200
        except Exception:
            traceback.print_exc()
            return INTERNAL_ERROR
        
def get_bios_settings(ident):
    if ident not in bios_setting:
        bios_setting[ident] = get_Bios_Settings_instance({'rb': '/redfish/v1/', 'id': ident})
    return bios_setting[ident]