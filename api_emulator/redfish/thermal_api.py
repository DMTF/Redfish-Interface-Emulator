#-----------------------------------------------------------------------------
# INTEL CONFIDENTIAL
# Copyright 2016 Intel Corporation All Rights Reserved.
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
Singleton API: GET, PATCH

"""
import g

import sys, traceback
from flask import Flask, request, make_response, render_template
from flask.ext.restful import reqparse, Api, Resource

from .templates.thermal import get_thermal_template

# config is instantiated by CreateThermal()
config = {}
INTERNAL_ERROR = 500

#Thermal API
class ThermalAPI(Resource):
    # Can't initialize the resource since the URI variables are not in the argument list.
    # Need the variables to set the Odata.id properties
    def __init__(self):
        print ('ThermalAPI init called')

    # HTTP GET
    def get(self,ch_id):
        try:
            global config
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PATCH
    def patch(self, ch_id):
        print ('ThermalAPI patch called')
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
class CreateThermal(object):
    def __init__(self):
        print ('CreateThermal init called')

    # PUT
    # - Create the resource (since URI variables are avaiable)
    def put(self,ch_id):
        print ('CreateThermal put called')
        try:
            global config
            config=get_thermal_template(g.rest_base,ch_id)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        print ('CreateThermal put exit')
        return resp
