# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Redfish Interface Emulator - main
#   python emulator.py

import os
import json
import argparse
import traceback
import xml.etree.ElementTree as ET

#import g

# Flask Imports
from flask import Flask, request, make_response, render_template
from flask.ext.restful import reqparse, Api, Resource

import g

# Emulator Imports
from api_emulator.resource_manager import ResourceManager
from api_emulator.exceptions import CreatePooledNodeError, ConfigurationError, RemovePooledNodeError
from api_emulator.resource_dictionary import ResourceDictionary 
from api_emulator import __version__
from scheduler import *

# Trays to load into the resource manager
TRAYS = None
SPEC = None
MODE=None

CONFIG = 'emulator-config.json'

# Base URL of the RESTful interface
REST_BASE = '/redfish/v1/'
g.rest_base = REST_BASE


# Creating the ResourceManager
resource_manager = None
resource_dictionary = None

# Parse REST request for Action
parser = reqparse.RequestParser()
parser.add_argument('Action', type=str, required=True)

# Read emulator-config file.
# If running on Cloud, use dyanaically assigned port
with open(CONFIG, 'r') as f:
    config = json.load(f)
    MODE = config['MODE']
if(MODE=='Cloud'):
    port = int(os.getenv("PORT"))

# Execution starts a main(), at end of file

def init_resource_manager():
    """
    Initializes the resource manager
    """
    global resource_manager
    global REST_BASE
    global TRAYS
    global SPEC
    resource_manager = ResourceManager(REST_BASE, SPEC,MODE,TRAYS)
    resource_dictionary = ResourceDictionary()


def error_response(msg, status, jsonify=False):
    data = {
        'Status': status,
        'Message': msg
    }
    if jsonify:
        data = json.dumps(data, indent=4)
    return data, status


INTERNAL_ERROR = error_response('Internal Server Error', 500)


class PathError(Exception):
    pass


@g.api.representation('application/json')
def output_json(data, code, headers=None):
    """
    Overriding how JSON is returned by the server so that it looks nice
    """
    resp = make_response(json.dumps(data, indent=4), code)
    resp.headers.extend(headers or {})
    return resp


class RedfishAPI(Resource):
    def __init__(self):
        # Dictionary of actions and their method
        self.actions = {
            'CreateGenericComputerSystem': self.create_system,
            'ApplySettings':self.update_system,
            'Reset': self.create_system,
            'Subscribe': self.subscribe_events }

        if resource_manager.spec == 'Redfish':
            self.system_path = 'Systems'
            self.chassis_path = 'Chassis'
            self.actions['ApplySettings']=self.update_system
            self.actions['Reset']=self.create_system
            self.actions['Subscribe']=self.subscribe_events

        super(RedfishAPI, self).__init__()


    def post(self, path):
        if path.find(self.system_path) != -1 or path.find(self.chassis_path) != -1:
            args = parser.parse_args()
            try:
                action = args['Action']
                path = path.split('/')
                if len(path) >= 2:
                    cs_puid = int(path[1])
                else:
                    cs_puid = 0
                resp = self.actions[action](action, cs_puid)
            except KeyError as e:
                traceback.print_exc()
                resp = error_response('Unknown action: {0}'.format(e.message), 400)
            except Exception:
                traceback.print_exc()
                resp = INTERNAL_ERROR
        elif path == 'EventService':
            args = parser.parse_args()
            try:
                action = args['Action']
                resp = self.actions[action](action)
            except KeyError as e:
                traceback.print_exc()
                resp = error_response('Unknown action: {0}'.format(e.message), 400)
            except Exception:
                traceback.print_exc()
                resp = INTERNAL_ERROR
        else:
            resp = '', 404
        return resp

        """
        Either return ServiceRoot or let resource manager handel
        """
    def get(self, path=None):

        try:
            if path is not None:
                # path has a value
                config = self.get_configuration(resource_manager, path)
            else:
                # path is None, fetch ServiceRoot
                config = resource_manager.configuration
            resp = config, 200
        except PathError:
            resp = error_response('Attribute Does Not Exist', 404)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    def delete(self, path):
        """
        Delete pooled node -- ONLY ALLOWS THE DELETION OF A POOLED NODE
        """
        try:
            path = path.split('/')
            assert len(path) == 2
            assert path[0] == self.system_path
            cs_puid = int(path[1])
            resource_manager.remove_pooled_node(cs_puid)
            resp = {'Message': 'Pooled node deleted successfully'}, 200
        except (AssertionError, ValueError):
            resp = error_response('Unknown DELETE request - this is only for pooled nodes', 404)
        except RemovePooledNodeError as e:
            resp = error_response(e.message, 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    @staticmethod
    def create_system(action, idx=1):
        global resource_manager
        try:
            assert request.json is not None, 'No JSON configuration given'
            if(action =='Reset'):
                cs_puid = idx
                config = resource_manager.update_cs(cs_puid,request.json)
            else:
                config = resource_manager._create_redfish(request.json, action)
            resp = config, 201
        except CreatePooledNodeError as e:
            resp = error_response(e.message, 406)
        except AssertionError as e:
            resp = error_response(e.message, 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    @staticmethod
    def update_system(action, idx=1):
        global resource_manager
        try:
            assert request.json is not None, 'No JSON configuration given'

            config = resource_manager.update_system(request.json, idx)
            resp = config, 201
        except CreatePooledNodeError as e:
            resp = error_response(e.message, 406)
        except AssertionError as e:
            resp = error_response(e.message, 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    @staticmethod
    def subscribe_events(action, idx=1):
        global resource_manager
        try:
            assert request.json is not None, 'No JSON configuration given'

            config = resource_manager.add_event_subscription(request.json)
            resp = config, 201
        except CreatePooledNodeError as e:
            resp = error_response(e.message, 406)
        except AssertionError as e:
            resp = error_response(e.message, 400)
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    @staticmethod
    def get_configuration(obj, path):
        """
        Helper function to follow the given path starting with the given object

        Arguments:
            obj  - Beginning object to start searching down.  obj should have a get_resource()
            path - Path of object to get

        """

        try:
            config = obj.get_resource(path)
        except (IndexError, AttributeError, TypeError, AssertionError, KeyError) as e:
            traceback.print_exc()
            raise PathError("Resource not found: " + str(e.message))
        return config

#
# If DELETE /redfish/v1/reset, then reset the resource manager
#
@g.app.route('/redfish/v1/reset/', methods=['DELETE'])
def reset():
    try:
        init_resource_manager()
        data = {'Message': 'Emulator reset successfully'}
        resp = json.dumps(data, indent=4), 200
    except Exception:
        traceback.print_exc()
        resp = error_response('Internal Server Error', 500, True)
    return resp


#
# If GET /, then return index.html (an intro page)
#
@g.app.route('/')
def index():
    return render_template('index.html')

#
# If any other RESTful request, send to RedfishAPI object for processing. Note: <path:path> specifies any path
#
g.api.add_resource(RedfishAPI, '/redfish/v1/', '/redfish/v1/<path:path>/')



def startup():
    """
    Startup method -- Reads in the configuration file
    """
    global CONFIG
    global TRAYS
    global SPEC
    global MODE

    with open(CONFIG, 'r') as f:
        config = json.load(f)

    TRAYS = config['TRAYS']
    SPEC = config['SPEC']
    MODE = config['MODE']

    assert SPEC == 'Redfish', \
        'Unknown spec: {0}, must be Redfish'.format(SPEC)

    init_resource_manager()


def main():
    """
    Main Method
    """
    global app
    global MODE

    with open(CONFIG, 'r') as f:
        config = json.load(f)

    HTTPS = config['HTTPS']
    MODE = config['MODE']
    if(MODE=='Cloud'):

        argparser = argparse.ArgumentParser(
        description='Redfish Manageability API Emulator - Version: ' + __version__,
        epilog='Developed by Intel')
        argparser.add_argument('-port', type=int, default=port,
                           help='Port to run the emulator on. Default define by Foundry')
        argparser.add_argument('-debug', action='store_true', default=False,
                           help='Run the emulator in debug mode. Note that if you'
                                ' run in debug mode, then the emulator will only'
                                'be ran locally.')
        args = argparser.parse_args()

    elif(MODE=='Local'):


        print (__version__)
        argparser = argparse.ArgumentParser(
        description='Redfish Manageability API Emulator - Version: ' + __version__,
        epilog='Developed by Intel')

        argparser.add_argument('-port', type=int, default=5000,
                           help='Port to run the emulator on. Default is 5000')
        argparser.add_argument('-debug', action='store_true', default=False,
                           help='Run the emulator in debug mode. Note that if you'
                                ' run in debug mode, then the emulator will only'
                                'be ran locally.')

        args = argparser.parse_args()

    try:
        startup()
        #schedule()
    except ConfigurationError as e:
        print ('Error Loading Trays:', e.message)
    else:
        if (HTTPS == 'Enable'):
            context = ('server.crt', 'server.key')
            kwargs = {'debug': args.debug, 'port': args.port, 'ssl_context' : context}
        else:
            kwargs = {'debug': args.debug, 'port': args.port}

        if not args.debug:
            kwargs['host'] = '0.0.0.0'

        print (' * Running in', SPEC, 'mode')
        g.app.run(**kwargs)

if __name__ == '__main__':
    main()
else:
    startup()
