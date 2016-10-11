# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Module for loading in static data (mockups)

import json
import os
import re

from .utils import process_id
from .exceptions import StaticLoadError
from .resource_dictionary import ResourceDictionary

class Member():
    def __init__(self, config):
        self.config = config

    @property
    def configuration(self):
        return self.config

def load_static(name, spec, rest_base, resource_dictionary):
    """
    Loads the static data starting at the directory ./<spec>/static/<name>, recursively.

    Populates the resdict dictionary, with the file path as the key.

    Expects a single index.json file in each directory.  Ignores other files.

    Arguments:
        name      - Name of the static data
        spec      - Which spec the data is under, must be either redfish
                    or chinook
        rest_base - Base URL of the RESTful interface
    """
    try:
        assert spec.lower() in ['redfish', 'chinook'], 'Unknown spec: ' + spec
        dirname = os.path.dirname(__file__)
        base_dir = os.path.join(dirname, spec.lower(), 'static')
        index = os.path.join(dirname, spec, 'static', name, 'index.json')
        assert os.path.exists(index), 'Static data for ' + name + ' does not exist'

        startDir = os.path.join(dirname, spec, 'static', name)
        for dirName, subdirList, fileList in os.walk(startDir):
    #	print('Found directory: %s' % dirName)
            for fname in fileList:
                if fname != 'index.json':
                    continue
                path = os.path.join(dirName,fname)
                f = open(path)
                index = json.load(f)
                m = Member(index)

                shortpath = re.sub(os.path.join(dirname, spec, 'static/'), '', path)
                shortpath = re.sub('/index.json', '', shortpath)
                resource_dictionary.add_resource(shortpath, m)
	# for x in resdict:
	#	print('Key: ')
	#	print(x)
	#	print('Value: ')
	#	print(resdict[x])

    except AssertionError as e:
        raise StaticLoadError(e.message)
    return shortpath
