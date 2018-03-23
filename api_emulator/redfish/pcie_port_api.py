# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/master/LICENSE.md

# PCIe Ports API  GET, POST
# PCIe Port  API  GET, PUT

import g
import traceback
# Flask Imports
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

from .templates.pcie_port import get_PCIePort_template

members = []
member_ids = []
INTERNAL_ERROR=500

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
            resp = make_response('Resources directory does not exist', 400)
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
            resp = make_response('Resources directory does not exist', 400)
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
            resp = make_response('Resources directory does not exist', 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # The POST command should be for addeding multiple instances
    def post(self,sw_id):
        try:
#            g.api.add_resource(PCIePortAPI, '/redfish/v1/PCIePorts/<string:ident>')
            resp=self.config,200
        except OSError:
            resp = make_response('Attribute Does Not Exist', 404)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp
