# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Declares global variables

from flask import Flask
from flask_restful import Api

# Base URI. Will get overwritten in emulator.py
rest_base = 'base'

# Create Flask server
app = Flask(__name__)

# Create RESTful API
api = Api(app)
