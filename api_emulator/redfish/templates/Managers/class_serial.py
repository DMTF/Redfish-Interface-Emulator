# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

from .serial_interface import get_serial_interface_template
from .serial_1 import get_serial_1_template
class SerialInterfaces(object):

    def __init__(self,rest_base):

        self.config=get_serial_1_template(rest_base)
        self.SerialInterface_1=get_serial_1_template(rest_base)

    @property
    def configuration(self):
        """
        Configuration property
        """
        c = self.config.copy()
        return c

