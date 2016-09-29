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
OVF Virtual System Representation
"""


class VirtualSystem(object):
    """
    VirtualSystem Representation

    This class the following important attributes:
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
