# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Singleton API: GET, PATCH

import g
import copy
import logging
import sys, traceback
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

from .templates.power import get_power_instance

# config is instantiated by CreatePower()
config = {}
INTERNAL_ERROR = 500

# Power API
class PowerAPI(Resource):
    # Can't initialize the resource since the URI variables are not in the argument list.
    # Need the variables to set the Odata.id properties
    def __init__(self, **kwargs):
        logging.info('PowerAPI init called')
        try:
            global config
            config=get_Power_instance(kwargs)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR

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
        logging.info('PowerAPI patch called')
        raw_dict = request.get_json(force=True)
        try:
            global config
            logging.debug(config)
            for key, value in raw_dict.items():
                print ('Update ' + key + ' to ' + value)
                config[key] = value
            logging.debug(config)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self):
         return 'PUT is not a valid command', 202

    # HTTP DELETE
    def delete(self,ch_id):
         return 'DELETE is not a valid command', 202

# Used to create a resource instance internally
class CreatePower(Resource):
    def __init__(self, **kwargs):
        logging.info('CreatePower init called')
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])
            logging.info(wildcards)
            logging.info(wildcards.keys())

    # PUT
    # - Create the resource (since URI variables are avaiable)
    def put(self,ch_id):
        logging.info('CreatePower put called')
        try:
            global config
            global wildcards
            config=get_power_instance(wildcards)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp
