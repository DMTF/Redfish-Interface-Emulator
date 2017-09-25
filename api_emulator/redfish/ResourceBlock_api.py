# Copyright Notice:
# Copyright 2017 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Example Collection Resource and Singleton Resource
"""
Collection API  GET, POST
Singleton  API  GET, POST, PATCH, DELETE

"""
import g

import sys, traceback
import logging
import copy
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

from .templates.ResourceBlock import get_ResourceBlock_instance
#from ResourceBlockProcessor_api import *


members = {}
INTERNAL_ERROR = 500

#Resource Block API
class ResourceBlockAPI(Resource):
    # kwargs is used to pass in the wildcards values to replace when the instance is created - via get_<resource>_instance().
    #
    # The call to attach the API, flask.add_resource(), establishes the contents of kwargs. All subsequent HTTP calls go through __init__.
    #   So __init__ stores kwargs in the wildcards variable and the wildcards is used in the other HTTP code.
    #
    def __init__(self, **kwargs):
        logging.info('ResourceBlockAPI init called')
        try:
            global config
            global wildcards
            wildcards = kwargs
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('ResourceBlockAPI init exit')

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

    def post(self,ident):
        return 'PUT is not a valid command', 202

    # HTTP PATCH
    def patch(self, ident):
        return 'PUT is not a valid command', 202


    # HTTP DELETE
    def delete(self,ident):
        return 'PUT is not a valid command', 202


# Resource Block Collection API
class ResourceBlockCollectionAPI(Resource):
    def __init__(self):
        self.rb = g.rest_base
        self.config = {
            '@odata.context': self.rb + '$metadata#ResourceBlockCollection.ResourceBlockCollection',
            '@odata.id': self.rb + 'ResourceBlockCollection',
            '@odata.type': '#ResourceBlockCollection.1.0.0.ResourceBlockCollection',
            'Name': 'Resource Block Collection',
            'Links': {}
        }
        self.config['Links']['Member@odata.count'] = len(members)
        self.config['Links']['Members'] = [{'@odata.id':x['@odata.id']} for x in members.values()]

    def get(self):
        try:
            resp = self.config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    def post(self):
        return 'PUT is not a valid command', 202




# CreateResourceBlock

class CreateResourceBlock(Resource):
    def __init__(self, **kwargs):
        logging.info('CreateResourceBlock init called')
        logging.debug(kwargs, kwargs.keys(), 'resource_class_kwargs' in kwargs)
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])
            logging.debug(wildcards, wildcards.keys())

    def put(self,ident):
        logging.info('CreateResourceBlock put called')
        try:
            global config
            global wildcards
            wildcards['id'] = ident
            config=get_ResourceBlock_instance(wildcards)
            members[ident]=config
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateResourceBlock init exit')
        return resp

    def post(self,ident,label,parameter):
        logging.info('CreateResourceBlock post called')
        try:
            global config
            global wildcards
            wildcards['linkProcessor'] = parameter
            if label == "processors":
                path = g.rest_base + "CompositionService/ResourceBlocks/" + ident + "/Processors/" + parameter
                logging.info('power path = ' + path)
                try:
                    g.api.add_resource(ResourceBlockProcessorAPI,   path, resource_class_kwargs={'rb': g.rest_base, 'ch_id': ident} )
                except:
                    pass
                config = CreateResourceBlockProcessor()
                out = config.__init__(resource_class_kwargs={'rb': g.rest_base,'ch_id': ident})
                #out = config.put("CPU-2")
            else:
                pass

            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateResourceBlock init exit')
        return resp

