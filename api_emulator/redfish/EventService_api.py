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
from .Subscriptions_api import SubscriptionCollectionAPI, SubscriptionAPI, CreateSubscription


# config is instantiated by CreateEventService()
config = {}
INTERNAL_ERROR = 500

# EventService API
class EventServiceAPI(Resource):
    def __init__(self, **kwargs):
        logging.info('EventServiceAPI init called')
        try:
            global config
            config=get_EventService_instance(kwargs)
            g.api.add_resource(SubscriptionCollectionAPI,   '/redfish/v1/EventService/Subscriptions')
            g.api.add_resource(SubscriptionAPI,             '/redfish/v1/EventService/Subscriptions/<string:id>')

            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateEventService put exit')

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
class CreateEventService(Resource):
    def __init__(self, **kwargs):
        logging.info('CreateEventService init called')
        logging.debug(kwargs)
        logging.debug(kwargs.keys())
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])
            logging.debug(wildcards)

    def put(self,ident):
        logging.info('CreateEventService put called')
        try:
            global config
            global wildcards
            wildcards['id'] = ident
            config=get_EventService_instance(wildcards)
            g.api.add_resource(SubscriptionCollectionAPI,   '/redfish/v1/EventService/Subscriptions')
            g.api.add_resource(SubscriptionAPI,             '/redfish/v1/EventService/Subscriptions/<string:ident>', resource_class_kwargs={'rb': g.rest_base})
            # Create an instance of subordinate subscription resource
            cfg = CreateSubscription()
            out = cfg.__init__(resource_class_kwargs={'rb': g.rest_base,'id':"1"})
            out = cfg.put("1")
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateEventService put exit')
        return resp
