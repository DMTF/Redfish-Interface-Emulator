# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# get_Chassis_Template()

import copy
import strgen

_TEMPLATE = \
    {
        "@odata.context": "{rb}$metadata#Chassis.Chassis",
        "@odata.id": "{rb}Chassis/{id}",
        "@odata.type": "#Chassis.v1_0_0.Chassis",
        "Id": "{id}",
        "Name": "Computer System Chassis",
        "ChassisType": "RackMount",
        "Manufacturer": "Redfish Computers",
        "Model": "3500RX",
        "SKU": "8675309",
        "SerialNumber": "437XR1138R2",
        "Version": "1.02",
        "PartNumber": "224071-J23",
        "AssetTag": "Chicago-45Z-2381",
        "Status": {
            "State": "Enabled",
            "Health": "OK"
        },
        "Thermal": {
            "@odata.id": "{rb}Chassis/{id}/Thermal"
        },
        "Power": {
            "@odata.id": "{rb}Chassis/{id}/Power"
        },
        "Links": {
            "ComputerSystems": [
                {
                    "@odata.id": "{rb}Systems/{linkSystem}"
                }
            ],
            "ManagedBy": [
                {
                    "@odata.id": "{rb}Managers/{linkMgr}"
                }
            ],
         },
    }


def get_Chassis_instance(wildcards):
    """
    Formats the template

    Arguments:
        rest_base - Base URL for the RESTful interface
        indent    - ID of the chassis
    """
    c = copy.deepcopy(_TEMPLATE)

    c['@odata.context'] = c['@odata.context'].format(**wildcards)
    c['@odata.id'] = c['@odata.id'].format(**wildcards)
    c['Id'] = c['Id'].format(**wildcards)
    c['Thermal']['@odata.id'] = c['Thermal']['@odata.id'].format(**wildcards)
    c['Power']['@odata.id'] = c['Power']['@odata.id'].format(**wildcards)
    c['Links']['ManagedBy'][0]['@odata.id'] = c['Links']['ManagedBy'][0]['@odata.id'].format(**wildcards)
    c['Links']['ComputerSystems'][0]['@odata.id']=c['Links']['ComputerSystems'][0]['@odata.id'].format(**wildcards)

    c['SerialNumber'] = strgen.StringGenerator('[A-Z]{3}[0-9]{10}').render()

    return c
