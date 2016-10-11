# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Virtual System Representation

class VirtualSystem(object):
    """
    VirtualSystem Representation

    This class has the following important attributes:
        proc_type     - Processor type for the virtual system
        processors    - Number of processors
        memory_gb     - Number of GB of memory
        disks         - List of simple_storage.Device objects
        network_ports - Number of network ports
    """
    def __init__(self):
        """
        VirtualSystem Constructor
        """
        self.proc_type = ''
        self.processors = 0
        self.memory_mb = 0
        self.disks = []
        self.network_connections = []

    def __str__(self):
        return \
        ('---- Virtual System ----\n'
         'Processor Type: {0}\n'
         '# Processors..: {1}\n'
         'Memory (MB)...: {2}\n'
         '# Disks.......: {3}\n'
         'Network.......: {4}\n').format(
            self.proc_type,
            self.processors,
            self.memory_mb,
            self.disks,
            self.network_connections)

    @property
    def network_ports(self):
        """
        Number of needed network ports
        """
        return len(self.network_connections)
