# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

Serial_1={
    "@odata.context": "{rb}$metadata#Managers/Links/Members/1/Links/SerialInterfaces/Links/Members/$entity",
    "@odata.id": "{rb}Managers/Manager_1/SerialInterfaces/SerialInterface_1",
    "@odata.type": "#SerialInterface.1.00.0.SerialInterface",
    "Name": "Managed Serial Interface 1",
    "Description": "Management for Serial Interface",
    "Status": {
        "State": "Enabled",
        "Health": "OK"
    },
    "SignalType": "Rs232",
    "BitRate": 115200,
    "Parity": "None",
    "DataBits": 8,
    "StopBits": 1,
    "FlowControl": "None",
    "PinOut": "Cyclades"
}


def get_serial_1_template(rest_base):
    c=Serial_1.copy()
    c['@odata.context']=c['@odata.context'].format(rb=rest_base)
    c['@odata.id']=c['@odata.id'].format(rb=rest_base)
    return c
