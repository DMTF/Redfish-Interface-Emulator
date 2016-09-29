#
# Copyright (c) 2016 Intel Corporation. All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# Neither the name of the Distributed Management Task Force (DMTF) nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

"""
Redfish Chassis Collection and Chassis Resource
"""
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
