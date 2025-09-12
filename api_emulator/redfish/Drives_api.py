import g
import sys, traceback
import logging
import copy
from flask import Flask, request, make_response
from flask_restful import reqparse, Api, Resource
from .templates.Drives import get_Drives_instance
drives_config={}
INTERNAL_ERROR=500
class Drives_API(Resource):
    def __init__(self, **kwargs):
        logging.info('DrivesAPI init called')
        self.rb = kwargs.get('rb', '')
    
    def get(self,ident):
        logging.info(f'DrivesAPI GET called')
        try:
            global drives_config
            drives_config=get_Drives_instance({'rb': self.rb, 'ch_id': ident})
            return drives_config, 200
        except Exception:
            traceback.print_exc()
            return INTERNAL_ERROR
    
    def post(self):
        return 'POST NOT SUPPORTED FOR DRIVES COLLECTION',405
    
    def patch(self):
        return 'PATCH NOT SUPPORTED FOR DRIVES COLLECTION',405

class CreateDrives(Resource):

    def __init__(self, **kwargs):
        logging.info('CreateDrives init called')
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])

    def put(self,ch_id):
        logging.info('CreateDrives put called')
        try:
            global config
            global wildcards
            wildcards['ch_id'] = ch_id
            config = get_Drives_instance(wildcards)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR  
        logging.info('CreateDrives init exit')
        return resp

    