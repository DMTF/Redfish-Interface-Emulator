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


MANAGERS_1={
    "@odata.context": "{rb}$metadata#Managers/Links/Members/$entity",
    "@odata.id": "{rb}Managers/Manager_1",
    "@odata.type": "#Managers.1.00.0.Manager",
    
    "Name": "Manager",
    "ManagerType": "BMC",
    "Description": "BMC",
    "UUID": "92384634-2938-2342-8820-489239905423",
    "Model": "Joo Janta 200",
    "Status": {
        "State": "Enabled",
        "Health": "OK"
    },
    "GraphicalConsole": {
        "Enabled": "true",
        "MaxConcurrentSessions": 2,
        "ConnectTypesSupported": [
            "KVMIP"
        ]
    },
    "SerialConsole": {
        "Enabled": "true",
        "MaxConcurrentSessions": 1,
        "ConnectTypesSupported": [
            "Telnet",
            "SSH",
            "IPMI"
        ]
    },
    "CommandShell": {
        "Enabled": "true",
        "MaxConcurrentSessions": 4,
        "ConnectTypesSupported": [
            "Telnet",
            "SSH"
        ]
    },
    "Firmware": {
        "Current": {
            "VersionString":"1.34g (build Aug 11 2014 10:59:46)"

        }
    },
    "Links": {
        "ManagerForServers": [{
                "@odata.id": "{rb}Systems/"
            }],
        "NetworkService": {
            "@odata.id": "{rb}Managers/Manager_1/NetworkService"
        },
        "EthernetNICs": {
            "@odata.id": "{rb}Managers/Manager_1/NICs"
        },
        "SerialInterfaces": {
            "@odata.id": "{rb}Managers/Manager_1/SerialInterfaces"
        },
        
        "VirtualMedia": {
            "@odata.id": "{rb}Managers/Manager_1/VM1"
        },
        "Oem": {}
    },
    "AvailableActions": [{"Action":"Reset"}],
        "Oem": {}
        
}




def get_managers_1_template(rest_base):


    c=MANAGERS_1.copy()
    c['@odata.context']=c['@odata.context'].format(rb=rest_base)
    c['@odata.id']=c['@odata.id'].format(rb=rest_base)
    c['Links']['ManagerForServers'][0]['@odata.id']=c['Links']['ManagerForServers'][0]['@odata.id'].format(rb=rest_base)
    c['Links']['NetworkService']['@odata.id']=c['Links']['NetworkService']['@odata.id'].format(rb=rest_base)
    c['Links']['EthernetNICs']['@odata.id']=c['Links']['EthernetNICs']['@odata.id'].format(rb=rest_base)
    c['Links']['SerialInterfaces']['@odata.id']= c['Links']['SerialInterfaces']['@odata.id'].format(rb=rest_base)
    c['Links']['VirtualMedia']['@odata.id']= c['Links']['VirtualMedia']['@odata.id'].format(rb=rest_base)
    return c
