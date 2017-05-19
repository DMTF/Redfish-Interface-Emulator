# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Singleton API: GET, PATCH

import g

import sys, traceback
from flask import Flask, request, make_response, render_template
from flask.ext.restful import reqparse, Api, Resource

from constants import PATHS
from .templates.power import get_power_template

# config is instantiated by CreatePower()
config = {}
INTERNAL_ERROR = 500

# Power API
class PowerAPI(Resource):
    # Can't initialize the resource since the URI variables are not in the argument list.
    # Need the variables to set the Odata.id properties
    def __init__(self):
        self.root = PATHS['Root']
        self.chassis = PATHS['Chassis']['path']
        self.power = PATHS['power']

    # HTTP GET
    def get(self, ch_id):
        try:
            global config
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PATCH
    def patch(self, ch_id):
        print ('PowerAPI patch called')
        raw_dict = request.get_json(force=True)
        print (raw_dict)
        try:
            global config
            print (config)
            for key, value in raw_dict.items():
                print ('Update ' + key + ' to ' + value)
                config[key] = value
            print (config)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self,ch_id):
         return 'PUT is not a valid command', 202

    # HTTP DELETE
    def delete(self,ch_id):
         return 'DELETE is not a valid command', 202

# Used to create a resource instance internally
class CreatePower(object):
    def __init__(self):
        print ('CreatePower init called')

    # PUT
    # - Create the resource (since URI variables are avaiable)
    def put(self,ch_id):
        print ('CreatePower put called')
        try:
            global config
            config=get_power_template(g.rest_base,ch_id)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        print ('CreatePower put exit')
        return resp
