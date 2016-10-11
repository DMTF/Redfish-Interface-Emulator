# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

SERIAL_INTERFACE={
    "@odata.context": "{rb}$metadata#Managers/1/Links/SerialInterfaces/$entity",
    "@odata.id": "{rb}Managers/1/SerialInterfaces",
    "@odata.type": "#SerialInterface.1.00.0.SerialInterfaceCollection",
    "Name": "Serial Interface Collection",
    "Description": "Collection of Serial Interfaces for this System",
    "Links": {
        "Members@odata.count":1,
        "Members": [
            {
                "@odata.id": "{rb}Managers/Manager_1/SerialInterfaces/SerialInterface_1"
            }
        ]
    }
}


def get_serial_interface_template(rest_base):
    c=SERIAL_INTERFACE.copy()
    c['@odata.context']=c['@odata.context'].format(rb=rest_base)
    c['@odata.type']=c['@odata.type'].format(rb=rest_base)
    c['Links']['Members'][0]['@odata.id']=c['Links']['Members'][0]['@odata.id'].format(rb=rest_base)
    return c
