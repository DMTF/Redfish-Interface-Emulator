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
Templates for the processor module
"""

PROCESSOR_TEMPLATE = {
    "@odata.context": "{rb}$metadata#{suffix}/Links/Members/{cs_puid}/Processors/Links/Members/$entity",
    "@odata.id": "{rb}{suffix}/{cs_puid}/Processors/{id}",
    "@odata.type": "#Processor.1.0.0.Processor",
    "Name":"Processor",
    "Id": None,
    "Socket": "CPU {socket}",
    "ProcessorType": "CPU",
    "ProcessorArchitecture": "x86",
    "InstructionSet": "x86-64",
    "Manufacturer": "Intel(R) Corporation",
    "Model": "Multi-Core Intel(R) Xeon(R) processor 7xxx Series",
    "ProcessorId":{
        "VendorId":"GenuineIntel",
        "IdentificationRegisters":"0x34AC34DC8901274A",
        "EffectiveFamily": "0x42",
        "EffectiveModel": "0x61",
        "Step": "0x1",
        "MicrocodeInfo": "0x429943"
  },
    "MaxSpeedMHz": None,
    "TotalCores": None,
    "TotalThreads": None,
    "Status": None
}


def format_processor_template(rb, suffix, cs_puid, ident, socket, max_mhx,
                              total_cores, enabled_cores, total_threads,
                              enabled_threads, status):
    """
    Format the processor template -- returns the template
    """
    c = PROCESSOR_TEMPLATE.copy()
    c['@odata.context'] = c['@odata.context'].format(rb=rb, suffix=suffix, cs_puid=cs_puid)
    c['@odata.id'] = c['@odata.id'].format(rb=rb, suffix=suffix, cs_puid=cs_puid, id=ident)
    c['Id'] = str(ident)
    c['Socket'] = c['Socket'].format(socket=socket)
    
    c['MaxSpeedMHz'] = max_mhx
    c['TotalCores'] = total_cores
    
    c['TotalThreads'] = total_threads
    
    c['Status'] = status
    return c
