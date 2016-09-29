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
PCIe Switches API  GET, POST
PCIe Switch   API  GET, PUT, PATCH, DELETE

"""
import g

import sys, traceback
from flask import Flask, request, make_response, render_template
from flask.ext.restful import reqparse, Api, Resource

from .templates.pcie_switch import get_PCIeSwitch_template
from .pcie_port_api import PCIePortsAPI, PCIePortAPI


members = []
member_ids = []
foo = 'false'
INTERNAL_ERROR = 500

#PCIe Switch API
class PCIeSwitchAPI(Resource):
    def __init__(self):
        print ('PCIeSwitchAPI init called')
        print ('PCIeSwitchAPI init exit')

    # HTTP GET
    def get(self,ident):
        try:
            # Find the entry with the correct value for Id
            for cfg in members:
                if (ident == cfg["Id"]):
                    break
            config = cfg
            resp = config, 200
        except OSError:
            resp = error_response('Resources directory does not exist', 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    # - On the first call, we add the API for PCIeSwitches, because sw_id is not available in 'init'.
    # - TODO - debug why this returns a 500 error, on the second put call
    def put(self,ident):
        print ('PCIeSwitchAPI put called')
        try:
            global config
            config=get_PCIeSwitch_template(g.rest_base,ident)
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']})
            global foo
            print ('var = ' + foo)
            g.api.add_resource(PCIePortsAPI, '/redfish/v1/PCIeSwitches/<string:sw_id>/Ports')
            g.api.add_resource(PCIePortAPI,  '/redfish/v1/PCIeSwitches/<string:sw_id>/Ports/<string:ident>')
            resp = config, 200
        except OSError:
            resp = error_response('Resources directory does not exist', 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        print ('PCIeSwitchAPI put exit')
        return resp

    # HTTP PATCH
    def patch(self, ident):
        print ('PCIeSwitchAPI patch called')
        raw_dict = request.get_json(force=True)
        print (raw_dict)
        try:
        # schema.validate(raw_dict)
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
        except OSError:
            resp = error_response('Resources directory does not exist', 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


    # HTTP DELETE
    def delete(self,ident):
        # print ('PCIeSwitchAPI delete called')
        try:
            idx = 0
            for cfg in members:
                if (ident == cfg["Id"]):
                    break
                idx += 1
            members.pop(idx)
            member_ids.pop(idx)
            resp = 200
        except OSError:
            resp = error_response('Resources directory does not exist', 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


# PCIe Switches API
class PCIeSwitchesAPI(Resource):
    def __init__(self):
        self.rb = g.rest_base
        self.config = {
            '@odata.context': self.rb + '$metadata#PCIeSwitches',
            '@odata.id': self.rb + 'PCIeSwitches',
            '@odata.type': '#PCIeSwitches.1.0.0.PCIeSwitches',
            'Name': 'PCIe Switches Collection',
            'Links': {}
        }
        self.config['Links']['Member@odata.count'] = len(member_ids)
        self.config['Links']['Members'] = member_ids

    def get(self):
        try:
            resp = self.config, 200
        except OSError:
            resp = error_response('Resources directory does not exist', 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # The POST command should be for adding multiple instances. For now, just add one.
    # Todo - Fix so the config can be passed in the data.
    def post(self):
        try:
            g.api.add_resource(PCIeSwitchAPI, '/redfish/v1/PCIeSwitches/<string:ident>')
            resp=self.config,200
        except PathError:
            resp = error_response('Attribute Does Not Exist', 404)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp
