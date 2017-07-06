# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# EventService_api.py
#
# Collection API  GET, POST
# Singleton  API  GET, PUT, PATCH, DELETE

import g

import sys, traceback
import logging
import copy
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

from .templates.EventService import get_EventService_instance
# from .events_api import EventCollectionAPI, EventAPI, CreateEvent
from .Subscriptions_api import SubscriptionCollectionAPI, SubscriptionAPI, CreateSubscription


# config is instantiated by CreatePower()
config = {}
INTERNAL_ERROR = 500

# EventService API
class EventServiceAPI(Resource):
    def __init__(self, **kwargs):
        print ('EventServiceAPI init called')
        try:
            global config
            config=get_EventService_instance(kwargs)
            g.api.add_resource(SubscriptionCollectionAPI,   '/redfish/v1/EventService/Subscriptions')
            g.api.add_resource(SubscriptionAPI,             '/redfish/v1/EventService/Subscriptions/<string:id>')

            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        print ('CreateEventService put exit')

    # HTTP GET
    def get(self):
        try:
            global config
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PATCH
    def patch(self):
         return 'PUT is not a valid command', 202

    # HTTP PUT
    def put(self):
         return 'PUT is not a valid command', 202

    # HTTP DELETE
    def delete(self):
         return 'DELETE is not a valid command', 202


# Used to create a resource instance internally
class CreateEventService(object):
    def __init__(self):
        print ('CreateEventService init called')

    # PUT
    # - Create the resource (since URI variables are avaiable)
    def put(self,ch_id):
        print ('CreateEventService put called')
        try:
            global config
            config=get_power_template(g.rest_base,ch_id)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        print ('CreateEventService put exit')
        return resp

members = []
member_ids = []
foo = 'false'

#EventService API
class EventServiceAPI2(Resource):
    # Can't initialize the resource since the URI variables are not in the argument list.
    # Need the variables to set the Odata.id properties
    def __init__(self):
        print ('EventServiceAPI init called')

    # HTTP GET
    def get(self,ident):
        try:
            # Find the entry with the correct value for Id
            for cfg in members:
                if (ident == cfg["Id"]):
                    break
            config = cfg
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT (don't need - can't replace EventService)
    # - Create the resource (since URI variables are avaiable)
    # - Update the members and members.id lists
    # - Attach the APIs of subordinate resources (do this only once)
    # - Finally, create an instance of the subordiante resources
    def put(self,ident):
        print ('EventServiceAPI put called')
        try:
            global config
            config=get_EventService_instance(g.rest_base,ident)
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']})
            global foo
            # Attach URIs for subordiante resources
            if  (foo == 'false'):
                g.api.add_resource(SubscriptionCollectionAPI,   '/redfish/v1/EventService/Subscriptions')
                g.api.add_resource(SubscriptionAPI,             '/redfish/v1/EventService/Subscriptions/<string:id>')
                foo = 'true'
            # Create an instance of subordinate resources
            cfg = CreateSubscription()
            out = cfg.__init__(resource_class_kwargs={'rb': g.rest_base,'id':"1"})
            out = cfg.put("1")

        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        print ('EventServiceAPI put exit')
        return resp

    # HTTP PATCH
    def patch(self, ident):
        print ('EventServiceAPI patch called')
        raw_dict = request.get_json(force=True)
        print (raw_dict)
        try:
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
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


    # HTTP DELETE
    def delete(self,ident):
        # print ('EventServiceAPI delete called')
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


# EventService Collection API
class EventServiceCollectionAPI(Resource):
    def __init__(self):
        self.rb = g.rest_base
        self.config = {
            '@odata.context': self.rb + '$metadata#EventServiceCollection',
            '@odata.id': self.rb + 'EventServiceCollection',
            '@odata.type': '#EventServiceCollection.1.0.0.EventServiceCollection',
            'Name': 'EventService Collection',
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
            g.api.add_resource(EventServiceAPI, '/redfish/v1/EventService/<string:ident>')
            resp=self.config,200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


# Used to create a resource instance internally
class CreateEventService(Resource):
    def __init__(self, **kwargs):
        print ('CreateEventService init called')
        logging.info(kwargs)
        logging.info(kwargs.keys())
        logging.info('resource_class_kwargs in kwargs')
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])
            logging.debug(wildcards, wildcards.keys())

    def put(self,ident):
        print ('CreateEventService put called')
        try:
            global config
            global wildcards
            config=get_EventService_instance(wildcards)
            members.append(config)
            member_ids.append({'@odata.id': config['@odata.id']})
            g.api.add_resource(SubscriptionCollectionAPI,   '/redfish/v1/EventService/Subscriptions')
            g.api.add_resource(SubscriptionAPI,             '/redfish/v1/EventService/Subscriptions/<string:ident>')
            # Create an instance of subordinate resources
            cfg = CreateSubscription()
            out = cfg.__init__(resource_class_kwargs={'rb': g.rest_base,'id':"1"})
            out = cfg.put("1")
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        print ('CreateEventService put exit')
        return resp
