# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md


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

