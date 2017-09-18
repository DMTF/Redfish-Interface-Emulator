# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Singleton API: POST

import g
import requests
import os
import subprocess
import time

import sys, traceback
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource
from subprocess import check_output

members={}
INTERNAL_ERROR = 500

class ResetAction_API(Resource):
    # kwargs is use to pass in the wildcards values to replace when the instance is created.
    def __init__(self, **kwargs):
        print ('ResetActionAPI init called')
        print ('init exit')

    # HTTP POST
    def post(self):
        print ('POST ActionInfoReset called')
#        cli= "ssh cumulus@10.223.197.159 sudo reboot"
#        clioutput = subprocess.call(cli, shell=True)
#        print (clioutput)
        print ('Reboot in progress')
        return 'POST request completed', 200

    # HTTP GET
    def get(self):
       return 'GET is not supported', 405, {'Allow': 'POST'}

    # HTTP PATCH
    def patch(self):
         return 'PATCH is not supported', 405, {'Allow': 'POST'}

    # HTTP PUT
    def put(self):
         return 'PUT is not supported', 405, {'Allow': 'POST'}

    # HTTP DELETE
    def delete(self):
         return 'DELETE is not supported', 405, {'Allow': 'POST'}
