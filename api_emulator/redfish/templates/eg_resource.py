# Copyright Notice:
# Copyright 2017 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Example Resoruce Template
import copy
import strgen

_EG_RESOURCE_TEMPLATE = \
    {
        "@odata.context": "{rb}$metadata#EgResource/Links/Members/$entity",
        "@odata.id": "{rb}EgResources/{id}",
        "@odata.type": "#EgResource.v1_0_0.EgResource",
        "Id": "{id}",
        "Name": "Name of Example Resource",
        "Description": "Need to add the properties to this resource's template.",
        "Manufacturer": "Redfish Computers",
        "SerialNumber": "437XR1138R2",
        "Version": "1.02",
        "PartNumber": "224071-J23",
        "Status": {
            "State": "Enabled",
            "Health": "OK"
        }
    }


def get_EgResource_template(rest_base, ident):
    """
    Formats the template

    Arguments:
        rest_base - Base URL for the RESTful interface
        indent    - ID of the resource
    """
    c = copy.deepcopy(_EG_RESOURCE_TEMPLATE)

    c['@odata.context'] = c['@odata.context'].format(rb=rest_base)
    c['@odata.id'] = c['@odata.id'].format(rb=rest_base, id=ident)
    c['Id'] = c['Id'].format(id=ident)

    c['SerialNumber'] = strgen.StringGenerator('[A-Z]{3}[0-9]{10}').render()

    return c
