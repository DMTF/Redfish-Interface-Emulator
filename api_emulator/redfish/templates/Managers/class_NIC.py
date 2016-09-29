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
            


        
