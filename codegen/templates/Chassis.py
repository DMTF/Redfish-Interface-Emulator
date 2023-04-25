#!/usr/bin/env python3
# Copyright Notice:
# Copyright 2017-2019 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/main/LICENSE.md

# Chassis.py

import copy
import strgen
from api_emulator.utils import replace_recurse

_TEMPLATE = \
{
    "@Redfish.Copyright": "Copyright 2014-2019 DMTF. All rights reserved.",
    "@odata.context": "/redfish/v1/$metadata#Chassis.Chassis",
    "@odata.id": "/redfish/v1/Chassis/1",
    "@odata.type": "#Chassis.v1_4_0.Chassis",
    "Id": "1",
    "Name": "Computer System Chassis",
    "ChassisType": "RackMount",
    "Manufacturer": "ManufacturerName",
    "Model": "ProductModelName",
    "SKU": "",
    "SerialNumber": "2M220100SL",
    "PartNumber": "",
    "AssetTag": "CustomerWritableThingy",
    "IndicatorLED": "Lit",
    "PowerState": "On",
    "Location" : {
        "@odata.type": "#Resource.v1_3_0.Location",
        "PostalAddress": {
            "Country": "US",
            "Territory": "TX",
            "District": "Harris",
            "City": "Houston",
            "Street": "TX-249",
            "HouseNumber": 19550,
            "Floor": "1",
            "Name": "Excellent dining establishment",
            "PostalCode": "77070-3002"
        },
        "Placement": {
            "Row": "North",
            "Rack": "WEB43",
            "RackOffsetUnits": "EIA_310",
            "RackOffset": 12
        }
    },
    "Status": {
        "State": "Enabled",
        "Health": "OK"
    },
	"HeightMm": 44.45,
	"WidthMm": 431.8,
	"DepthMm": 711,
	"WeightKg": 15.31,
    "Thermal": {
        "@odata.id": "/redfish/v1/Chassis/1/Thermal"
    },
    "Power": {
        "@odata.id": "/redfish/v1/Chassis/1/Power"
    },
    "NetworkAdapters": {
        "@odata.id": "/redfish/v1/Chassis/1/NetworkAdapters"
    },
    "Links": {
        "ComputerSystems": [
            {
                "@odata.id": "/redfish/v1/Systems/1"
            }
        ],
        "ContainedBy": {
            "@odata.id": "/redfish/v1/Chassis/Rack1"
        },
        "ManagedBy": [
            {
                "@odata.id": "/redfish/v1/Managers/1"
            }
        ],
        "ManagersInChassis": [
            {
                "@odata.id": "/redfish/v1/Managers/1"
            }
        ],
        "PCIeDevices": [
            {"@odata.id": "/redfish/v1/Chassis/1/PCIeDevices/NIC"}
        ],
        "Oem": {}
    },
    "Oem": {}
}


def get_Chassis_instance(wildcards):
    c = copy.deepcopy(_TEMPLATE)
    replace_recurse(c, wildcards)
    return c
