# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

VM={
    "@odata.context": "{rb}$metadata#Managers/Links/Members/1/Links/VirtualMedia/$entity",
    "@odata.id": "{rb}Managers_1/VirtualMedia",
    "@odata.type": "#VirtualMedia.1.00.0.VirtualMediaCollection",
    "Name": "Virtual Media Services",
    "Description": "iLO Virtual Media Services Settings",
    "Total": 2,
    "Links": {
        "Members@odata.count": 2,
        "Members": [
            {
                "@odata.id": "{rb}Managers/Manager_1/VM1/Floppy1"
            },
            {
                "@odata.id": "{rb}Managers/Manager_1/VM1/CD1"
            }
        ]
    }
}


def get_VM1_template(rest_base):
    c=VM.copy()
    c['@odata.context']=c['@odata.context'].format(rb=rest_base)
    c['@odata.type']=c['@odata.type'].format(rb=rest_base)
    c['Links']['Members'][0]['@odata.id']=c['Links']['Members'][0]['@odata.id'].format(rb=rest_base)
    c['Links']['Members'][1]['@odata.id']=c['Links']['Members'][1]['@odata.id'].format(rb=rest_base)
    return c
