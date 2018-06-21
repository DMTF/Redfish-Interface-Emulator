# Copyright Notice:
# Copyright 2017-2018 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/master/LICENSE.md

# Example Subresource Collection Resource or Singleton Resource API file
#
# Replace the string "EgSubResource" with the proper resource
# names and adjust the code as necessary for the HTTP commands.
#
# This API file goes in the api_emulator/redfish directory, and must
# be paired with an appropriate SubResource template file in the
# api_emulator/redfish/templates directory. The resource_manager.py
# file in the api_emulator directory can then be edited to use these
# files to make the resource dynamic.

"""
These APIs get attached to subordinate Collection Resources or
subordinate Singleton Resources. They are attached by the resource
to which they are subordinate.

Collection API:  GET, POST
Singleton  API:  GET, POST, PATCH, DELETE
"""

import g

import sys, traceback
import logging
import copy
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

# SubResource imports
from .templates.eg_subresource import get_EgSubResource_instance

members = []
member_ids = []
foo = 'false'
INTERNAL_ERROR = 500


# EgSubResource API

class EgSubResourceAPI(Resource):

    # kwargs is used to pass in the wildcards values to be replaced
    # when the instance is created via get_<resource>_instance().
    #
    # The call to attach the API establishes the contents of kwargs.
    # All subsequent HTTP calls go through __init__.
    #
    # __init__ stores kwargs in the wildcards variable which is used
    # to pass the wildcards to the HTTP code.
    def __init__(self, **kwargs):
        logging.info('EgSubResourceAPI init called')
        logging.debug(kwargs)
        try:
            global config
            global wildcards
            wildcards = kwargs
        except Exception:
            traceback.print_exc()
        logging.info('EgSubResourceAPI init exit')

    # HTTP GET
    def get(self,ident):
        try:
            # Find the entry with the correct value for Id
            resp = 404
            for cfg in members:
                if (ident == cfg["Id"]):
                    config = cfg
                    resp = config, 200
                    break
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP POST
    # - Create the resource using the available URI variables
    # - Update the members and members.id lists
    def post(self,ident):
        logging.info('EgSubResourceAPI POST called')
        try:
            global config
            global wildcards
            wildcards['id']= ident
            config=get_EgSubResource_instance(wildcards)
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']})
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('EgSubResourceAPI POST exit')
        return resp

    # HTTP PATCH
    def patch(self, ident):
        logging.info('EgSubResourceAPI PATCH called')
        raw_dict = request.get_json(force=True)
        logging.info(raw_dict)
        try:
            # Update specific portions of the identified object
            logging.info(members[ident])
            for key, value in raw_dict.items():
                logging.info('Update ' + key + ' to ' + str(value))
                members[ident][key] = value
            logging.info(members[ident])
            resp = members[ident], 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP DELETE
    def delete(self, ident):
        # logging.info('EgSubResourceAPI DELETE called')
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


# EgSubResourceCollection API

class EgSubResourceCollectionAPI(Resource):
    def __init__(self, **kwargs):
        logging.info('EgSubResourceCollectionAPI init called')
        logging.debug(kwargs)
        odatapath = kwargs['path']
        self.config = {
            '@odata.context': g.rest_base + '$metadata#EgSubResourceCollection.EgSubResourceCollection',
            '@odata.type': '#EgSubResourceCollection.1.0.0.EgSubResourceCollection',
            '@odata.id': odatapath,
            'Name': 'EgSubResource Collection',
            'Links': {}
        }
        self.config['Links']['Member@odata.count'] = len(member_ids)
        self.config['Links']['Members'] = member_ids

    # HTTP GET
    def get(self):
        logging.info('EgSubResourceCollectionAPI GET called')
        try:
            resp = self.config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP POST
    # Todo - 'id' should be obtained from the request data.
    def post(self):
        logging.info('EgSubResourceCollectionAPI POST called')
        try:
            global wildcards
            wildcards['id']= 'Test2'
            config=get_EgSubResource_instance(wildcards)
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']})
            resp=self.config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


# CreateEgSubResource
#
# Called internally to create instances of a subresource. If the
# resource has subordinate resources, those subordinate resource(s)
# are created automatically.
#
# This routine can also be used to pre-populate the emulator with
# resource instances, such as a Chassis and a ComputerSystem. (See
# examples in resource_manager.py.)
#
# Note: This is not the optimal way to pre-populate the emulator,
# because the resource_manager.py file must be edited. A better way
# would be to create a program file (e.g. populate.py) which performs
# a POST for each resource instance desired. Multiple such 'populate'
# files could then be used without making changes to the emulator.
# 
# Note: In 'init', the first time through, kwargs may not have any
# values, so we need to check. The call to 'init' stores the path
# wildcards. The wildcards are used to modify the resource template
# when subsequent calls are made to instantiate resources.

class CreateEgSubResource(Resource):
    def __init__(self, **kwargs):
        logging.info('CreateEgSubResource init called')
        logging.debug(kwargs, kwargs.keys(), 'resource_class_kwargs' in kwargs)
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])
            logging.debug(wildcards, wildcards.keys())

    # Attach APIs for subordinate resource(s). Attach the APIs for
    # a resource collection and its singletons.
    def put(self,ident):
        logging.info('CreateEgSubResource PUT called')
        try:
            global config
            global wildcards
            config=get_EgSubResource_instance(wildcards)
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']})
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateEgSubResource PUT exit')
        return resp
