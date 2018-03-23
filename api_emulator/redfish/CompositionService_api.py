# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/master/LICENSE.md

# CompositionService_api.py
#
# Collection API  GET, POST
# Singleton  API  GET, PUT, PATCH, DELETE

import g

import sys, traceback
import logging
import copy
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

from .templates.CompositionService import get_CompositionService_instance

# config is instantiated by CreateCompositionService()
config = {}
INTERNAL_ERROR = 500

# CompositionService API
class CompositionServiceAPI(Resource):
    def __init__(self, **kwargs):
        logging.info('CompositionServiceAPI init called')
        try:
            global config
            config=get_CompositionService_instance(kwargs)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateCompositionService put exit')

    # HTTP GET
    def get(self):
        try:
            global config
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PATCH
    def patch(self):
         return 'PUT is not a valid command', 202

    # HTTP PUT
    def put(self):
         return 'PUT is not a valid command', 202

    # HTTP DELETE
    def delete(self):
         return 'DELETE is not a valid command', 202


