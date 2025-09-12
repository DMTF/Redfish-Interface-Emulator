import g
import sys, traceback
import logging
import copy
from flask import Flask, request, make_response
from flask_restful import reqparse, Api, Resource
from .templates.Drive import get_Drive_instance
from .Drives_api import drives_config

drive_config={}
drives = ["Drive-1", "Drive-2", "Drive-3", "Drive-4", "Drive-5", "Drive-6"]
INTERNAL_ERROR=500
class Drive_API(Resource):
    def __init__(self, **kwargs):
        logging.info('DrivesAPI init called')
        self.rb = kwargs.get('rb', '')
    
    def get(self,ident,ident1):
        logging.info(f'DrivesAPI GET called')
        try:
            global drive_config
            if ident1 not in drives:
                logging.warning(f"Drive {ident1} not found under Chassis {ident}")
                return {"error": f"Drive {ident1} not found under Chassis {ident}"}, 404

            if ident not in drive_config:
                drive_config[ident] = {}
            if ident1 not in drive_config[ident]:
                drive_config[ident][ident1]=get_Drive_instance({'rb': self.rb, 'ch_id': ident,'dr_id':ident1})
            return drive_config[ident][ident1], 200
        except Exception:
            traceback.print_exc()
            return INTERNAL_ERROR
    
    def post(self):
        return 'POST NOT SUPPORTED FOR DRIVES COLLECTION',405
    
    def patch(self):
        return 'PATCH NOT SUPPORTED FOR DRIVES COLLECTION',405

class CreateDrive(Resource):

    def __init__(self, **kwargs):
        logging.info('CreateDrive init called')
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])

    def put(self):
        logging.info('CreateDrives put called')
        try:
            global config
            global wildcards
            config = get_Drive_instance(wildcards)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR  
        logging.info('CreateDrive init exit')
        return resp

    