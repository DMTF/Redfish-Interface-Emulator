# Copyright Notice:
# Copyright 2017-2018 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/master/LICENSE.md

# Manager Collection Resource and Singleton Resource
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

from .templates.Manager import get_Manager_instance

# from .eg_subresource_api import EgSubResourceCollectionAPI, EgSubResourceAPI, CreateEgSubResource

members = {}
foo = 'false'
INTERNAL_ERROR = 500


# Manager API
class ManagerAPI(Resource):
    # kwargs is used to pass in the wildcards values to replace when the instance is created - via get_<resource>_instance().
    #
    # __init__ should store the wildcards and pass the wildcards to the get_<resource>_instance(). 
    def __init__(self, **kwargs):
#        logging.basicConfig(level=logging.INFO)
        logging.debug('ManagerAPI init called')
        try:
            global config
            global wildcards
            wildcards = kwargs
        #            config=get_Manager_instance(wildcards)
        #            resp = config, 200
        except Exception:
            traceback.print_exc()
        #            resp = INTERNAL_ERROR
        logging.debug('ManagerAPI init exit')

    # HTTP GET
    def get(self, ident):
        try:
            # Find the entry with the correct value for Id
            resp = 404
            if ident in members:
                resp = members[ident], 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP POST
    # - Create the resource (since URI variables are avaiable)
    # - Update the members and members.id lists
    # - Attach the APIs of subordinate resources (do this only once)
    # - Finally, create an instance of the subordiante resources
    def post(self, ident):
        logging.info('ManagerAPI PUT called')
        try:
            global wildcards
            wildcards['id'] = ident
            config = get_Manager_instance(wildcards)
            members[ident] = config
            global foo
            # Attach URIs for subordiante resources
            '''
            if  (foo == 'false'):
                # Add APIs for subordinate resourcs
                collectionpath = g.rest_base + "Managers/" + ident + "/EgSubResources"
                logging.info('collectionpath = ' + collectionpath)
                g.api.add_resource(EgSubResourceCollectionAPI, collectionpath, resource_class_kwargs={'path': collectionpath} )
                singletonpath = collectionpath + "/<string:ident>"
                logging.info('singletonpath = ' + singletonpath)
                g.api.add_resource(EgSubResourceAPI, singletonpath,  resource_class_kwargs={'rb': g.rest_base, 'eg_id': ident} )
                foo = 'true'
            '''
            # Create an instance of subordinate resources
            # cfg = CreateSubordinateRes()
            # out = cfg.put(ident)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('ManagerAPI put exit')
        return resp

    # HTTP PATCH
    def patch(self, ident):
        logging.info('ManagerAPI PATCH called')
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
        # logging.info('ManagerAPI delete called')
        try:
            resp = 404
            if ident in members:
                del (members[ident])
                resp = 200
        except Exception as e:
            traceback.print_exc()
            print (e)
            resp = INTERNAL_ERROR
        return resp


# Manager Collection API
class ManagerCollectionAPI(Resource):
    def __init__(self):
        self.rb = g.rest_base
        self.config = {
            '@odata.context': self.rb + '$metadata#ManagerCollection.ManagerCollection',
            '@odata.id': self.rb + 'Managers',
            '@odata.type': '#ManagerCollection.1.0.0.ManagerCollection',
            'Name': 'Manager Collection',
            'Links': {}
        }

    def get(self):
        try:
            self.config['Links']['Member@odata.count'] = len(members)
            self.config['Links']['Members'] = [{'@odata.id':x['@odata.id']} for
                    x in list(members.values())]
            resp = self.config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # The POST command should be for adding multiple instances. For now, just add one.
    # Todo - Fix so the config can be passed in the data.
    def post(self,ident):
        try:
            config=request.get_json(force=True)
            config['@odata.id']='redfish/v1/'

            resp = self.config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


# CreateManager
#
# Called internally to create a instances of a resource.  If the resource has subordinate resources,
# those subordinate resource(s)  should be created automatically.
#
# This routine can also be used to pre-populate emulator with resource instances.  For example, a couple of
# Chassis and a Manager (see examples in resource_manager.py)
#
# Note: this may not the optimal way to pre-populate the emulator, since the resource_manager.py files needs
# to be editted.  A better method is just hack up a copy of usertest.py which performs a POST for each resource
# instance desired (e.g. populate.py).  Then one could have a multiple 'populate' files and the emulator doesn't
# need to change.
# 
# Note: In 'init', the first time through, kwargs may not have any values, so we need to check.
#   The call to 'init' stores the path wildcards. The wildcards are used when subsequent calls instanctiate
#   resources to modify the resource template.
#
class CreateManager(Resource):
    def __init__(self, **kwargs):
        logging.info('CreateManager init called')
        logging.debug(kwargs)  # , kwargs.keys(), 'resource_class_kwargs' in kwargs)
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])
            logging.debug(wildcards)  # , wildcards.keys())

    # Attach APIs for subordinate resource(s). Attach the APIs for a resource collection and its singletons
    def put(self, ident):
        logging.info('CreateManager put called')
        try:
            global wildcards
            wildcards['id'] = ident
            config = get_Manager_instance(wildcards)
            members[ident] = config
            '''
            # attach subordinate resources
            collectionpath = g.rest_base + "Managers/" + ident + "/EgSubResources"
            logging.info('collectionpath = ' + collectionpath)
            g.api.add_resource(EgSubResourceCollectionAPI, collectionpath, resource_class_kwargs={'path': collectionpath} )
            singletonpath = collectionpath + "/<string:ident>"
            logging.debug('singletonpath = ' + singletonpath)
            g.api.add_resource(EgSubResourceAPI, singletonpath,  resource_class_kwargs={'rb': g.rest_base, 'eg_id': ident} )
            '''
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateManager init exit')
        return resp
