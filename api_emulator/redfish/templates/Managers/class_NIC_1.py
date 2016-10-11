# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

from .NIC_1 import get_NIC_1_template
from .NIC_1 import NIC_1
from .SD_temp import get_SD_template
from api_emulator.exceptions import CreatePooledNodeError

class NICs_1(object):

    def __init__(self,config,rest_base):
        self.rb=rest_base
        self.config= {}
        self.SD=get_SD_template(rest_base)
        self.configure(config)

    @property
    def configuration(self):
        """
        Configuration property
        """
        config=self.config.copy()
        return self.config

    def configure(self,config):
        self._base_configure()
        self.config['SpeedMbps']=int(config['SpeedMbps'])


    def _base_configure(self):
        try:

            self.config=NIC_1.copy()
            self.odata_id = self.config['@odata.id'].format(rb=self.rb)
            self.config['@odata.context'] = self.config['@odata.context'].format(rb=self.rb)
            self.config['@odata.id'] = self.odata_id
        except KeyError as e:
            raise CreatePooledNodeError(
                'Incorrect configuration, missing key: ' + e.message)

