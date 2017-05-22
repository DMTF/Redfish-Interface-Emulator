# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Singleton API: GET, PATCH

import g

import sys, traceback
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

from .templates.ietf_interfaces__interfaces_state__statistics import create_Statistics_instance

config = {}
INTERNAL_ERROR = 500

class StatisticsAPI(Resource):
    # kwargs is use to pass in the wildcards values to replace when the instance is created.
    def __init__(self, **kwargs):
        print ('StatisticsAPI init called')
        print (kwargs)
        sw_id = kwargs['{sw_id}']
        if_state_id = kwargs['{if_state_id}']
        try:
            global config
            config=create_Statistics_instance(g.rest_base,sw_id,if_state_id)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        print ('Statistics init exit')

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
        print ('StatisticsAPI patch called')
        raw_dict = request.get_json(force=True)
        print (raw_dict)
        try:
            global config
            print (config)
            for key, value in raw_dict.items():
                config[key] = value
#            print (config)
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
