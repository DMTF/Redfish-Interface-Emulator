# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Redfish Chassis Collection and Chassis Resource

import strgen

from .templates.redfish_chassis import get_chassis_template
from .templates.misc_metrics import get_misc_metrics_template
from .templates.power_metrics import get_power_metrics_template
from .templates.thermal_metrics import get_thermal_metrics_template

# import sys
# sys.path.append('..')
# from ..resource_manager import add_resource

class Chassis(object):
    """
    Chassis class based on Chassis.1.0.0.Chassis
    """
    def __init__(self, rest_base, ident):
        """
        Chassis Constructor

        Arguments:
            rest_base - Base URL of the RESTful interface
            ident     - Identifier of the chassis
        """
        self.config = get_chassis_template(rest_base, ident)
        self.MiscMetrics = get_misc_metrics_template(rest_base, ident)
        self.PowerMetrics = get_power_metrics_template(rest_base, ident)
        self.ThermalMetrics = get_thermal_metrics_template(rest_base, ident)

    @property
    def configuration(self):
        """
        Configuration property
	    Create a copy of the Chassis dictionary, then fix it up.
        """
        config = self.config.copy()

        # Change to random string - 3 letters and 10 digits
        config['SerialNumber'] = strgen.StringGenerator('[A-Z]{3}[0-9]{10}').render()

        return config

    def update(self,config):
        for key in config:
            self.config[key]=config[key]


class ChassisCollection(object):
    """
    ChassisCollection class based on ChassisCollection.1.0.0.ChassisCollection
    """
    def __init__(self, rest_base):
        """
        ChassisCollection Constructor

        Inserts a placeholder for the Links property.  The Links property will be set
	when configuration() is called.

	Arguments:
            rest_base - Base URL of the RESTful interface
        """
        self.rb = rest_base
        self.members = []
        self.member_ids = []

        self.config = {
            '@odata.context': self.rb + '$metadata#Chassis',
            '@odata.id': self.rb + 'Chassis',
            '@odata.type': '#Chassis.1.0.0.ChassisCollection',
            'Name': 'Chassis Collection',
            'Links': {}
        }


    def __getitem__(self, idx):
        return self.members[idx - 1]

    def update_member(self,rs,idx):
        self.members[idx - 1].update(rs)

    @property
    def configuration(self):
        """
        Configuration property
	Copy the default dictionary and add the Links entries. Return the new dictionary.
        """
        c = self.config.copy()
        c['Links']['Member@odata.count'] = len(self.member_ids)
        c['Links']['Members'] = self.member_ids
        return c

    def add_chassis(self):
        """
        Creates a Chassis object and adds it to the local member and member_id
	dictionaries.
	Returns the chassis object
        """
        c = Chassis(self.rb, len(self.members) + 1)
        self.members.append(c)
        self.member_ids.append(c.configuration['@odata.id'])
        return c
