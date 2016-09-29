#-----------------------------------------------------------------------------
# INTEL CONFIDENTIAL
# Copyright 2015 Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related to
# the source code ("Material") are owned by Intel Corporation or its suppliers
# or licensors. Title to the Material remains with Intel Corporation or its
# suppliers and licensors. The Material contains trade secrets and proprietary
# and confidential information of Intel or its suppliers and licensors. The
# Material is protected by worldwide copyright and trade secret laws and
# treaty provisions. No part of the Material may be used, copied, reproduced,
# modified, published, uploaded, posted, transmitted, distributed, or
# disclosed in any way without Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be
# express and approved by Intel in writing.
#-----------------------------------------------------------------------------
"""
Collection API  GET, POST
Singleton  API  GET, PUT, PATCH, DELETE

"""
import g

import sys, traceback
from flask import Flask, request, make_response, render_template
from flask.ext.restful import reqparse, Api, Resource

from .templates.chassis import get_Chassis_template
from .thermal_api import ThermalAPI, CreateThermal
from .power_api import PowerAPI, CreatePower


members = []
member_ids = []
foo = 'false'
INTERNAL_ERROR = 500

#Chassis API
class ChassisAPI(Resource):
    # Can't initialize the resource since the URI variables are not in the argument list.
    # Need the variables to set the Odata.id properties
    def __init__(self):
        print ('ChassisAPI init called')

    # HTTP GET
    def get(self,ident):
        try:
            # Find the entry with the correct value for Id
            for cfg in members:
                if (ident == cfg["Id"]):
                    break
            config = cfg
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    # - Create the resource (since URI variables are avaiable)
    # - Update the members and members.id lists
    # - Attach the APIs of subordinate resources (do this only once)
    # - Finally, create an instance of the subordiante resources
    def put(self,ident):
        print ('ChassisAPI put called')
        try:
            global config
            config=get_Chassis_template(g.rest_base,ident)
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']})
            global foo
            # Attach URIs for subordiante resources
            if  (foo == 'false'):
                g.api.add_resource(ThermalAPI, '/redfish/v1/Chassis/<string:ch_id>/Thermal')
                g.api.add_resource(PowerAPI,   '/redfish/v1/Chassis/<string:ch_id>/Power')
                foo = 'true'
            # Create instances of subordinate resources, then call put operation
            cfg = CreateThermal()
            out = cfg.put(ident)
            cfg = CreatePower()
            out = cfg.put(ident)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        print ('ChassisAPI put exit')
        return resp

    # HTTP PATCH
    def patch(self, ident):
        print ('ChassisAPI patch called')
        raw_dict = request.get_json(force=True)
        print (raw_dict)
        try:
            # Find the entry with the correct value for Id
            for cfg in members:
                if (ident == cfg["Id"]):
                    break
            config = cfg
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


    # HTTP DELETE
    def delete(self,ident):
        # print ('ChassisAPI delete called')
        try:
            idx = 0
            for cfg in members:
                if (ident == cfg["Id"]):
                    break
                idx += 1
            members.pop(idx)
            member_ids.pop(idx)
            resp = 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


# Chassis Collection API (Chassis has the same form for singular and plural)
class ChassisCollectionAPI(Resource):
    def __init__(self):
        self.rb = g.rest_base
        self.config = {
            '@odata.context': self.rb + '$metadata#ChassisCollection',
            '@odata.id': self.rb + 'ChassisCollection',
            '@odata.type': '#ChassisCollection.1.0.0.ChassisCollection',
            'Name': 'Chassis Collection',
            'Links': {}
        }
        self.config['Links']['Member@odata.count'] = len(member_ids)
        self.config['Links']['Members'] = member_ids

    def get(self):
        try:
            resp = self.config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # The POST command should be for adding multiple instances. For now, just add one.
    # Todo - Fix so the config can be passed in the data.
    def post(self):
        try:
            g.api.add_resource(ChassisAPI, '/redfish/v1/Chassis/<string:ident>')
            resp=self.config,200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


# Used to create a resource instance internally
class CreateChassis(object):
    def __init__(self):
        print ('CreateChassis init called')

    def put(self,ident):
        print ('CreateChassis put called')
        try:
            global config
            config=get_Chassis_template(g.rest_base,ident)
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']})
            g.api.add_resource(ThermalAPI, '/redfish/v1/Chassis/<string:ch_id>/Thermal')
            g.api.add_resource(PowerAPI, '/redfish/v1/Chassis/<string:ch_id>/Power')
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        print ('CreateChassis put exit')
        return resp
