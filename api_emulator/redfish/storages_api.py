import g
import sys, traceback
import logging
import copy
from flask import Flask, request, make_response
from flask_restful import reqparse, Api, Resource
from .templates.storages import get_Storages_instance
drives_config={}
INTERNAL_ERROR=500
class Storages_API(Resource):
    def __init__(self, **kwargs):
        logging.info('StorageAPI init called')
        self.rb = kwargs.get('rb', '')
    
    
    def get(self,ident):
        logging.info(f'StoragesAPI GET called')
        try:
            global drives_config
            system_number = ident.split("-")[-1]
            chassis_id = f"Chassis-{system_number}"
            drives_config=get_Storages_instance({'rb': self.rb, 'id': ident,'ch_id':chassis_id})  
            return drives_config, 200
        except Exception:
            traceback.print_exc()
            return INTERNAL_ERROR
    
    def post(self):
        return 'POST NOT SUPPORTED FOR DRIVES COLLECTION',405
    
    def patch(self):
        return 'PATCH NOT SUPPORTED FOR DRIVES COLLECTION',405

class CreateStorages(Resource):

    def __init__(self, **kwargs):
        logging.info('CreateStorage init called')
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])

    def put(self,id):
        logging.info('CreateDrives put called')
        try:
            global config
            global wildcards
            system_number = id.split("-")[-1]
            chassis_id = f"Chassis-{system_number}"
            wildcards['ch_id']=chassis_id
            wildcards['id'] = id
            config = get_Storages_instance(wildcards)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR  
        logging.info('CreateStorage init exit')
        return resp

    