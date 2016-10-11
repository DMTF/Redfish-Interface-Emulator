# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

CD={
    "@odata.context": "{rb}$metadata#Managers/Links/Members/1/Links/VirtualMedia/Links/Members/$entity",
    "@odata.id": "{rb}Managers/Manager_1/VirtualMedia/CD1",
    "@odata.type": "#VirtualMedia.1.00.0.VirtualMedia",

    "Name": "Virtual CD",

    "MediaTypes": [
        "CD",
        "DVD"
    ],
    "Image": "irc://<only add this if http path someserver/mymedia-puttable.iso>",
    "ImageName": "mymedia-read-only.iso",
    "ConnectedVia": "Applet",
    "Inserted": "true",
    "WriteProtected": "false"
}

def get_CD_template(rest_base):

    c=CD.copy()
    c['@odata.context']=c['@odata.context'].format(rb=rest_base)
    c['@odata.id']=c['@odata.id'].format(rb=rest_base)
    return c
