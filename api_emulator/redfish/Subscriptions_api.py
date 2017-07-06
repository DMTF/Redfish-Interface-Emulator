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

from .templates.Subscription import get_Subscription_instance

members = []
member_ids = []
foo = 'false'
INTERNAL_ERROR = 500

#Subscription API
class SubscriptionAPI(Resource):
    # kwargs is used to pass in the wildcards values to replace when the instance is created - via get_<resource>_instance().
    #
    # __init__ should store the wildcards and pass the wildcards to the get_<resource>_instance(). 
    def __init__(self, **kwargs):
        logging.basicConfig(level=logging.INFO)
        logging.info('SubscriptionAPI init called')
        try:
            global config
            global wildcards
#            wildcards = kwargs
            config=get_Subscription_instance(wildcards)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('SubscriptionAPI init exit')

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
    # - Create the resource (since URI variables are avaiable)
    # - Update the members and members.id lists
    # - Attach the APIs of subordinate resources (do this only once)
    # - Finally, create an instance of the subordiante resources
    def post(self,ident):
#        logging.info('SubscriptionAPI put called')
        print('SubscriptionAPI put called')
        try:
            global config
            global wildcard
            config=get_Subscription_instance(wildcards)
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']})
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('SubscriptionAPI put exit')
        return resp

    # HTTP PATCH
    def patch(self, ident):
        logging.info('SubscriptionAPI patch called')
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
    def delete(self,ident):
        # logging.info('SubscriptionAPI delete called')
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


# Subscription Collection API
class SubscriptionCollectionAPI(Resource):
    def __init__(self):
        self.rb = g.rest_base
        self.config = {
            '@odata.context': self.rb + '$metadata#SubscriptionCollection.SubscriptionCollection',
            '@odata.id': self.rb + 'SubscriptionCollection',
            '@odata.type': '#SubscriptionCollection.1.0.0.SubscriptionCollection',
            'Name': 'Subscription Collection',
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
            g.api.add_resource(SubscriptionAPI, '/redfish/v1/EventService/Subscriptions/<string:ident>')
            resp=self.config,200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


# CreateSubscription
#
# Called internally to create a instances of a resource.  If the resource has subordinate resources,
# those subordinate resource(s)  should be created automatically.
#
# This routine can also be used to pre-populate emulator with resource instances.  For example, a couple of
# Chassis and a ComputerSystem (see examples in resource_manager.py)
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
class CreateSubscription(Resource):
    def __init__(self, **kwargs):
        logging.info('CreateSubscription init called')
        logging.debug(kwargs, kwargs.keys(), 'resource_class_kwargs' in kwargs)
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])
            logging.debug(wildcards, wildcards.keys())

    def put(self,ident):
        logging.info('CreateSubscription put called')
        try:
            global config
            global wildcards
            config=get_Subscription_instance(wildcards)
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']})
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateSubscription init exit')
        return resp
