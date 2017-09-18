# Copyright Notice:
# Copyright 2017 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Example Collection Resource or Singleton Resource API file
#
# Replace the strings "EgResource" and "EgSubResource" with
# the proper resource names and adjust the code as necessary for the
# HTTP commands.
#
# This API file goes in the api_emulator/redfish directory, and must
# be paired with an appropriate Resource template file in the
# api_emulator/redfish/templates directory. The resource_manager.py
# file in the api_emulator directory can then be edited to use these
# files to make the resource dynamic.

"""
These APIs get attached to Collection Resources or Singleton
Resources.

Collection API:  GET, POST
Singleton  API:  GET, POST, PATCH, DELETE
"""

import g

import sys, traceback
import logging
import copy
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

# Resource and SubResource imports
from .templates.eg_resource import get_EgResource_instance
from .eg_subresource_api import EgSubResourceCollectionAPI, EgSubResourceAPI, CreateEgSubResource

members = []
member_ids = []
foo = 'false'
INTERNAL_ERROR = 500


# EgResource API

class EgResourceAPI(Resource):

    # kwargs is used to pass in the wildcards values to be replaced
    # when the instance is created via get_<resource>_instance().
    #
    # The call to attach the API establishes the contents of kwargs.
    # All subsequent HTTP calls go through __init__.
    #
    # __init__ stores kwargs in the wildcards variable which is used
    # to pass the wildcards to the get_<resource>_instance() call.

    def __init__(self, **kwargs):
        logging.basicConfig(level=logging.INFO)
        logging.info('EgResourceAPI init called')
        try:
            global config
            global wildcards
            config=get_EgResource_instance(wildcards)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('EgResourceAPI init exit')


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
    # - Attach the APIs of subordinate resources (done only once)
    # - Finally, create instances of the subordinate resources

    def post(self,ident):
        logging.info('EgResourceAPI POST called')
        print('EgResourceAPI put called')
        try:
            global config
            config=get_EgResource_instance({'rb': g.rest_base, 'eg_id': ident})
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']})
            global foo
            # Attach URIs for subordinate resources
            if  (foo == 'false'):
                # Add APIs for subordinate resourcs
                collectionpath = g.rest_base + "EgResources/" + ident + "/EgSubResources"
                logging.info('collectionpath = ' + collectionpath)
                g.api.add_resource(EgSubResourceCollectionAPI, collectionpath, resource_class_kwargs={'path': collectionpath} )
                singletonpath = collectionpath + "/<string:ident>"
                logging.info('singletonpath = ' + singletonpath)
                g.api.add_resource(EgSubResourceAPI, singletonpath,  resource_class_kwargs={'rb': g.rest_base, 'eg_id': ident} )
                foo = 'true'
            # Create an instance of subordinate resources
            #cfg = CreateSubordinateRes()
            #out = cfg.put(ident)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('EgResourceAPI POST exit')
        return resp


    # HTTP PATCH

    def patch(self, ident):
        logging.info('EgResourceAPI PATCH called')
        raw_dict = request.get_json(force=True)
        logging.info(raw_dict)
        try:
            # Find the entry with the correct value for Id
            for cfg in members:
                if (ident == cfg["Id"]):
                    break
            config = cfg
            logging.info(config)
            for key, value in raw_dict.items():
                logging.info('Update ' + key + ' to ' + value)
                config[key] = value
            logging.info(config)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


    # HTTP DELETE

    def delete(self, ident):
        # logging.info('EgResourceAPI DELETE called')
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


# EgResource Collection API

class EgResourceCollectionAPI(Resource):
    def __init__(self):
        self.rb = g.rest_base
        self.config = {
            '@odata.context': self.rb + '$metadata#EgResourceCollection',
            '@odata.id': self.rb + 'EgResourceCollection',
            '@odata.type': '#EgResourceCollection.1.0.0.EgResourceCollection',
            'Name': 'EgResource Collection',
            'Links': {}
        }
        self.config['Links']['Member@odata.count'] = len(member_ids)
        self.config['Links']['Members'] = member_ids


    # HTTP GET

    def get(self):
        try:
            resp = self.config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


    # HTTP POST
    # POST should allow adding multiple instances to a collection.
    # For now, this only adds one instance.
    # Todo - Fix so the config can be passed in as an argument.

    def post(self):
        try:
            g.api.add_resource(EgResourceAPI, '/redfish/v1/EgResources/<string:ident>')
            resp=self.config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


# CreateEgResource
#
# Called internally to create instances of a resource. If the
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

class CreateEgResource(Resource):
    def __init__(self, **kwargs):
        logging.info('CreateEgResource init called')
        logging.debug(kwargs) #, kwargs.keys(), 'resource_class_kwargs' in kwargs)
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])
            logging.debug(wildcards)#, wildcards.keys())

    # Attach APIs for subordinate resource(s). Attach the APIs for
    # a resource collection and its singletons.

    def put(self,ident):
        logging.info('CreateEgResource PUT called')
        try:
            global config
            global wildcards
            wildcards['id'] = ident
            config=get_EgResource_instance(wildcards)
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']})
            # Attach subordinate resources
            collectionpath = g.rest_base + "EgResources/" + ident + "/EgSubResources"
            logging.info('collectionpath = ' + collectionpath)
            g.api.add_resource(EgSubResourceCollectionAPI, collectionpath, resource_class_kwargs={'path': collectionpath} )
            singletonpath = collectionpath + "/<string:ident>"
            logging.debug('singletonpath = ' + singletonpath)
            g.api.add_resource(EgSubResourceAPI, singletonpath,  resource_class_kwargs={'rb': g.rest_base, 'eg_id': ident} )
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateEgResource PUT exit')
        return resp
