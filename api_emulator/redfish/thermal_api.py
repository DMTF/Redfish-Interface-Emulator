# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/master/LICENSE.md

# Singleton API: GET, PATCH

import g
import copy
import logging
import sys, traceback
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

from .templates.thermal import get_thermal_instance

# config is instantiated by CreateThermal()
members={}
INTERNAL_ERROR = 500

#Thermal API
class ThermalAPI(Resource):
    # Can't initialize the resource since the URI variables are not in the argument list.
    # Need the variables to set the Odata.id properties
    def __init__(self, **kwargs):
        logging.info('ThermalAPI init called')

    # HTTP GET
    def get(self,ident):
        try:
            # Find the entry with the correct value for Id
            resp = 404
            if ident in members:
                resp = members[ident], 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PATCH
    def patch(self):
        logging.info('ThermalAPI patch called')
        raw_dict = request.get_json(force=True)
        try:
            global config
            for key, value in raw_dict.items():
                print ('Update ' + key + ' to ' + value)
                config[key] = value
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self):
         return 'PUT is not a valid command', 202

    # HTTP DELETE
    def delete(self):
         return 'DELETE is not a valid command', 202

# Used to create a resource instance internally
class CreateThermal(Resource):
    def __init__(self, **kwargs):
        logging.info('CreateThermal init called')
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])
            logging.debug(wildcards)#, wildcards.keys())

    # PUT
    # - Create the resource (since URI variables are avaiable)
    def put(self,ch_id):
        logging.info('CreateThermal put called')
        try:
            global wildcards
            config=get_thermal_instance(wildcards)
            members[ch_id]=config
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp
