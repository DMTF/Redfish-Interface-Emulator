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


NETWORK_SERVICE={
    "@odata.context": "{rb}$metadata#Managers/Links/Members/1/Links/NetworkService/$entity",
    "@odata.id": "{rb}Managers/Manager_1/NetworkService",
    "@odata.type": "#ManagerNetworkService.1.00.0.ManagerNetworkService",
    
    "Name": "Manager Network Service",
    "Description": "Manager Network Service Status",
    "Status": {
        "State": "Enabled",
        "Health": "OK"
    },
    "HostName": "web483-bmc",
    "FQDN": "mymanager.mydomain.com",
    "HTTP": {
        "Enabled": "true",
        "Port": "80"
    },
    "HTTPS": {
        "Enabled": "true",
        "Port": "443"
    },
    "IPMI": {
        "Enabled": "true",
        "Port": "623"
    },
    "SSH": {
        "Enabled": "true",
        "Port": "22"
    },
    "SNMP": {
        "Enabled": "true",
        "Port": "161"
    },
    "VirtualMedia": {
        "Enabled": "true",
        "Port": "17988"
    },
    "SSDP": {
        "Enabled": "true",
        "Port": "1900",
        "NotifyMulticastIntervalSeconds": "600",
        "NotifyTTL": "5",
        "NotifyIPv6Scope": "Site"
    },
    "Telnet": {
        "Enabled": "true",
        "Port": "23"
    },
    "KVMIP": {
        "Enabled": "true",
        "Port": "5288"
    },
    "Oem": {}
}

def get_network_service(rest_base):

    c=NETWORK_SERVICE.copy()
    c['@odata.context']=c['@odata.context'].format(rb=rest_base)
    c['@odata.id']=c['@odata.id'].format(rb=rest_base)

    return c

