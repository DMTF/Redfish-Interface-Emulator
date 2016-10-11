# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

from .NIC import get_NIC_template
from .NIC_1 import get_NIC_1_template
from .class_NIC_1 import NICs_1
from .NIC_1 import NIC_1

class NIC(object):

    def __init__(self,rest_base):
        self.rb=rest_base
        self.rs={}
        self.configure(self.rs)
        self.config=get_NIC_template(rest_base)
        self.NIC_1= NICs_1(self.rs,rest_base)


    @property
    def configuration(self):
        """
        Configuration property

        """

        c = self.config.copy()
        return c


    def configure(self,rs):

        self._base_configure()
        self.rs['SpeedMbps']=int(self.rs['SpeedMbps'])


    def _base_configure(self):

        try:
            self.rs=NIC_1.copy()
            self.odata_id = self.rs['@odata.id'].format(rb=self.rb)
            self.rs['@odata.context'] = self.rs['@odata.context'].format(rb=self.rb)
            self.rs['@odata.id'] = self.odata_id
        except KeyError as e:
            raise CreatePooledNodeError(
                'Incorrect configuration, missing key: ' + e.message)

