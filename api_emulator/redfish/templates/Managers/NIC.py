# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

NIC={
    "@odata.context": "{rb}$metadata#Managers/Links/Members/1/Links/NICs/$entity",
    "@odata.id": "{rb}Managers/1/NICs",
    "@odata.type": "#EthernetNetworkInterface.1.00.0.EthernetNetworkInterfaceCollection",
    "Name": "NICs Collection",
    "Description": "Collection of NICs for this Manager",
    "Links": {
        "Members@odata.count":1,
        "Members": [
            {
                "@odata.id": "{rb}Managers/Manager_1/NICs/NIC_1"
            }
        ]
    }
}


def get_NIC_template(rest_base):
    c=NIC.copy()
    c['@odata.context']=c['@odata.context'].format(rb=rest_base)
    c['@odata.type']=c['@odata.type'].format(rb=rest_base)
    c['Links']['Members'][0]['@odata.id']=c['Links']['Members'][0]['@odata.id'].format(rb=rest_base)
    return c
