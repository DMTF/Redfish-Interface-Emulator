# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

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
    "AvailableActions": [{"Action":"Reset"}]
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
