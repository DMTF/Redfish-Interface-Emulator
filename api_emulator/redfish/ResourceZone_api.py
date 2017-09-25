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

from .templates.ResourceZone import get_ResourceZone_instance

members = {}
INTERNAL_ERROR = 500

#Resource Zone API
class ResourceZoneAPI(Resource):
    # kwargs is used to pass in the wildcards values to replace when the instance is created - via get_<resource>_instance().
    #
    # The call to attach the API, flask.add_resource(), establishes the contents of kwargs. All subsequent HTTP calls go through __init__.
    #   So __init__ stores kwargs in the wildcards variable and the wildcards is used in the other HTTP code.
    #
    def __init__(self, **kwargs):
        logging.info('ResourceZoneAPI init called')
        try:
            global config
            global wildcards
            wildcards = kwargs
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('ResourceZoneAPI init exit')

    # HTTP GET
    def get(self,ident):
        try:
            # Find the entry with the correct value for Id
            resp = 404
            if ident in members:
                resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP POST
    # - Create the resource (since URI variables are avaiable)
    # - Update the members and members.id lists
    # - Attach the APIs of subordinate resources (do this only once)
    # - Finally, create an instance of the subordiante resources


    def post(self,ident):
        return 'PUT is not a valid command', 202

    # HTTP PATCH
    def patch(self, ident):
        return 'PUT is not a valid command', 202


    # HTTP DELETE
    def delete(self,ident):
        return 'PUT is not a valid command', 202


# Resource Zone Collection API
class ResourceZoneCollectionAPI(Resource):
    def __init__(self):
        self.rb = g.rest_base
        self.config = {
            '@odata.context': self.rb + '$metadata#ResourceZoneCollection.ResourceZoneCollection',
            '@odata.id': self.rb + 'ResourceZoneCollection',
            '@odata.type': '#ResourceZoneCollection.1.0.0.ResourceZoneCollection',
            'Name': 'Resource Zone Collection',
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


# CreateResourceZone
class CreateResourceZone(Resource):
    def __init__(self, **kwargs):
        logging.info('CreateResourceZone init called')
        logging.debug(kwargs, kwargs.keys(), 'resource_class_kwargs' in kwargs)
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])
            logging.debug(wildcards, wildcards.keys())

    def put(self,ident):
        logging.info('CreateResourceZone put called')
        try:
            global config
            global wildcards
            wildcards['id'] = ident
            config=get_ResourceZone_instance(wildcards)
            members[ident]=config
            #members.append(config)
            #member_ids.append({'@odata.id': config['@odata.id']})
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateResourceZone init exit')
        return resp
