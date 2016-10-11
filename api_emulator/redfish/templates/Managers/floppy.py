# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

Floppy={
    "@odata.context": "{rb}$metadata#Managers/Links/Members/1/Links/VirtualMedia/Links/Members/$entity",
    "@odata.id": "{rb}Managers/Manager_1/VirtualMedia/Floppy1",
    "@odata.type": "#VirtualMedia.1.00.VirtualMedia", 
    "Name": "Virtual Removable Media",
    "MediaTypes": [
        "Floppy",
        "USBStick"
    ],
    "Image": "irc://<only add this if http path someserver/mymedia-puttable.img>",
    "ImageName": "mymedia-read-only.img",
    "ConnectedVia": "URI",
    "Inserted": "true",
    "WriteProtected": "false"
}


def get_floppy_template(rest_base):

    c=Floppy.copy()
    c['@odata.context']=c['@odata.context'].format(rb=rest_base)
    c['@odata.id']=c['@odata.id'].format(rb=rest_base)
    return c
