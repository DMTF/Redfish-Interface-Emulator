# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# get_Chassis_instance()

import copy
import strgen
from api_emulator.utils import replace_recurse

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
    Creates an instace of TEMPLATE and replace wildcards as specfied
    """
    c = copy.deepcopy(_TEMPLATE)
    replace_recurse(c, wildcards)
    # print ("fini c: ", c)
    return c
