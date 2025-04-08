import g
import sys, traceback
import logging
import copy
from flask import Flask, request, make_response
from flask_restful import reqparse, Api, Resource

# Resource and SubResource imports
from .templates.Bios import get_Bios_instance

bios_config = {}
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
            if ident not in bios_config:
                bios_config = get_Bios_instance({'rb': self.rb, 'id': ident})  
            return bios_config, 200
        except Exception:
            traceback.print_exc()
            return INTERNAL_ERROR
        
def get_bios_config(ident):
    """
    Returns the current bios_config
    """
    try:
        global bios_config
        # Pass the extracted 'ident' (system ID) to get_Bios_instance
        bios_config = get_Bios_instance({'rb': '/redfish/v1/', 'id': ident})  
        return bios_config
    except Exception:
        traceback.print_exc()
    return bios_config

def set_bios_config(ident, data):
    """
    Sets bios_config[ident] by calling get_Bios_instance.
    You can call this from any other module.
    """
    try:
        global bios_config
        if ident not in bios_config:
            bios_config[ident] = get_Bios_instance({'rb': "/redfish/v1/", 'id': ident})
        
        for key, value in data['Attributes'].items():
                bios_config[ident]['Attributes'][key] = value
                
    except Exception as e:
        logging.error(f"Error setting BIOS config: {e}")
        traceback.print_exc()