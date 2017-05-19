# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Declares global variables

from flask import Flask
from flask.ext.restful import Api

# Base URI. Will get overwritten in emulator.py
rest_base = 'base'

# Create Flask server
app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'xxxxx@gmail.com'
app.config['MAIL_PASSWORD'] = 'xxxxxx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Create RESTful API
api = Api(app)
