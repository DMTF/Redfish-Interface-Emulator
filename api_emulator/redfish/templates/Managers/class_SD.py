# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

from .SD_temp import get_SD_template

class class_SD(object):

    def __init__(self,rest_base):

        self.config=get_SD_template(rest_base)


    @property
    def configuration(self):
        """
        Configuration property
        """
        c = self.config.copy()
        return c
