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
Redfish Processors and Processor Resources

Based on version 1.0.0
"""
from api_emulator.utils import timestamp
from .templates.processor import format_processor_template


class Processor(object):
    """
    Processor.1.0.0.Processor
    """
    def __init__(self, rest_base, suffix, cs_puid, ident, socket, max_mhx,
                  total_cores, enabled_cores, total_threads,
                  enabled_threads, status):
        """
        Processor Constructor

        Arguments:
            rest_base - Base URL for the REST server
        """
        self.rb = rest_base
        self._config = format_processor_template(rest_base, suffix, cs_puid, ident, socket,
                                                 max_mhx, total_cores, enabled_cores, total_cores,
                                                 enabled_cores, status)
        self.odata_id = self._config['@odata.id']

    @property
    def configuration(self):
        """
        Configuration Property
        """
        return self._config.copy()


class Processors(object):
    """
    Processor.1.0.0.ProcessorCollection
    """
    def __init__(self, rest_base, suffix, cs_puid):
        """
        Processors Constructor
        """
        self.rest_base = rest_base
        self.members = []
        self.member_ids = []
        self.odata_id = '{0}{1}/{2}/Processors'.format(rest_base, suffix, cs_puid)

        self._config = {
            '@odata.context': '{0}$metadata{1}/{2}/Links/Processors/$entity'.format(rest_base, suffix, cs_puid),
            '@odata.id': self.odata_id,
            '@odata.type': '#Processor.1.00.0.ProcessorCollection',
            'Name': 'Processor Collection',
            
            'Links': {}
        }

    def __getitem__(self, idx):
        return self.members[idx - 1]

    @property
    def configuration(self):
        """
        Configuration Property
        """
        c = self._config.copy()
        c['Links']['Members@odata.count'] = len(self.member_ids)
        c['Links']['Members'] = self.member_ids
        return c

    def add_processor(self, proc):
        """
        Adds the given processor to the collection
        """
        self.member_ids.append({'@odata.id': proc.odata_id})
        self.members.append(proc)


