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
ComputerSystems Module
"""
#from api_emulator.utils import timestamp
rest_base='/redfish/v1'

class ComputerSystemCollection(object):
    """
    PooledNodeCollection Class
    """

    def __init__(self, rest_base):
        """
        PooledNodeCollection Constructor
        """
        #self.modified = timestamp()
        self.systems = {}

    def __getitem__(self, idx):
        print 'Index is...%s...'%idx
        return self.systems[idx]

    @property
    def configuration(self):
        """
        Configuration Property
        """
        systems = []

        for pn in self.systems:
            print pn
            pn = self.systems[pn]
            systems.append({'@odata.id': pn.odata_id})

        return {
            '@odata.context': '/redfish/v1/$metadata#Systems',
            '@odata.type': '#ComputerSystem.1.0.0.ComputerSystemCollection',
            '@odata.id': '/redfish/v1/Systems',
            'Name': 'Computer System Collection',
            
            'Links': {
                'Members@odata.count': len(systems),
                'Members': systems
            }
        }

    @property
    def count(self):
        """
        Number of pooled nodes
        """
        return len(self.systems.keys())

    def add_computer_system(self, cs):
        """
        Add the given ComputerSystem to the collection
        """
        self.systems[cs.cs_puid] = cs

    def remove_computer_system(self, cs):
        """
        Removing the given ComputerSystem
        """
        del self.systems[cs.cs_puid]




