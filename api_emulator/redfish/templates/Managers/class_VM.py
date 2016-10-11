# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

from .VM1 import get_VM1_template
from .CD import get_CD_template
from .floppy import get_floppy_template
from .class_NIC_1 import NICs_1

class VM(object):

    def __init__(self,rest_base):

        self.config=get_VM1_template(rest_base)
        self.CD1= get_CD_template(rest_base)
        self.Floppy1=get_floppy_template(rest_base)


    @property
    def configuration(self):
        """
        Configuration property
        """
        c = self.config.copy()
        return c
