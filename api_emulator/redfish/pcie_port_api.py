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
PCIe Ports API  GET, POST
PCIe Port  API  GET, PUT

"""
import g

# Flask Imports
from flask import Flask, request, make_response, render_template
from flask.ext.restful import reqparse, Api, Resource

from .templates.pcie_port import get_PCIePort_template

members = []
member_ids = []

#PCIe Port API
class PCIePortAPI(Resource):
    def __init__(self):
        # Attach the dependent resources
        print ('PCIePortAPI init called')

    def get(self,sw_id,ident):
        try:
            global config
            resp = config, 200
        except OSError:
            resp = error_response('Resources directory does not exist', 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    def put(self,sw_id,ident):
        try:
            global config
            config=get_PCIePort_template(g.rest_base,sw_id,ident)
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']} )
            resp = config, 200
        except OSError:
            resp = error_response('Resources directory does not exist', 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

# PCIe Ports API
class PCIePortsAPI(Resource):
    def __init__(self):
        print ('PCIePortsAPI init called')
        self.rb = g.rest_base

        self.config = {
            '@odata.context': self.rb + '$metadata#PCIePorts',
            '@odata.id': self.rb + 'PCIePorts',
            '@odata.type': '#PCIePorts.1.0.0.PCIePorts',
            'Name': 'PCIe Ports Collection',
            'Links': {}
        }
        self.config['Links']['Member@odata.count'] = len(member_ids)
        self.config['Links']['Members'] = member_ids
        print ('PCIePortsAPI exit called')

    def get(self,sw_id):
        print ('PCIePortAPI get called')
        try:
            self.config['@odata.id'] = self.rb + 'Switches/' + sw_id + '/PCIePorts'
            resp = self.config, 200
        except OSError:
            resp = error_response('Resources directory does not exist', 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # The POST command should be for addeding multiple instances
    def post(self,sw_id):
        try:
#            g.api.add_resource(PCIePortAPI, '/redfish/v1/PCIePorts/<string:ident>')
            resp=self.config,200
        except PathError:
            resp = error_response('Attribute Does Not Exist', 404)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp
