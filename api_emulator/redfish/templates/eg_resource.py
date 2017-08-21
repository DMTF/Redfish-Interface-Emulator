# Copyright Notice:
# Copyright 2017 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Example Resoruce Template
import copy
import strgen
from api_emulator.utils import replace_recurse

_TEMPLATE = \
    {
        "@odata.context": "{rb}$metadata#EgResource.EgResource",
        "@odata.type": "#EgResource.v1_0_0.EgResource",
        "@odata.id": "{rb}EgResources/{id}",
        "Id": "{id}",
        "Name": "Name of Example Resource",
        "Description": "Example resource.",
        "Manufacturer": "Redfish Computers",
        "SerialNumber": "437XR1138R2",
        "Version": "1.02",
        "PartNumber": "224071-J23",
        "Status": {
            "State": "Enabled",
            "Health": "OK"
        },
        "SubResources": {
            "@odata.id": "{rb}EgResources/{id}/EgSubResources"
        }
    }

def get_EgResource_instance(wildcards):
    """
    Creates an instace of TEMPLATE and replace wildcards as specfied.  Also
    set any unique values.

    Arguments:
        wildcard - A dictionary of wildcards strings and their replacement values
    """
    c = copy.deepcopy(_TEMPLATE)
    replace_recurse(c, wildcards)
    # print ("fini c: ", c)

    c['SerialNumber'] = strgen.StringGenerator('[A-Z]{3}[0-9]{10}').render()

    return c
