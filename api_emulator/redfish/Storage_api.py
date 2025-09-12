import g
import sys, traceback
import logging
import copy
from flask import Flask, request, make_response
from flask_restful import reqparse, Api, Resource
from .templates.Storage import get_Storage_instance
from api_emulator.redfish.storages_api import CreateStorages
from .templates.storages import get_Storages_instance
drives_config={}
INTERNAL_ERROR=500
class Storage_API(Resource):
    def __init__(self, **kwargs):
        logging.info('StorageAPI init called')
        self.rb = kwargs.get('rb', '')
    
    
    def get(self,ident):
        logging.info(f'StorageAPI GET called')
        try:
            global drives_config
            drives_config=get_Storage_instance({'rb': self.rb, 'id': ident})  
            return drives_config, 200
        except Exception:
            traceback.print_exc()
            return INTERNAL_ERROR
    
    def post(self):
        return 'POST NOT SUPPORTED FOR DRIVES COLLECTION',405
    
    def patch(self):
        return 'PATCH NOT SUPPORTED FOR DRIVES COLLECTION',405

class CreateStorage(Resource):

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
            wildcards['id'] = id
            config = get_Storage_instance(wildcards)
            resp = config,200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR  
        logging.info('CreateStorage init exit')
        return resp

    