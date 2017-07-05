# Copyright Notice:
# Copyright 2017 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Example Resoruce Template
import copy
import strgen

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

# not used
def get_EgResource_instance(rest_base, ident):
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

def get_EgResource_instance2(wildcards):
    """
    Formats the template

    Arguments:
        wildcard - A dictionary of wildcards strings and their repalcement values

    dict={"key1":"string","key2":"placeholders"}
    msg='This {key1} contains custom {key2}'.format(**dict)

    """
    c = copy.deepcopy(_TEMPLATE)

    c['@odata.context'] = c['@odata.context'].format(**wildcards)
    c['@odata.id'] = c['@odata.id'].format(**wildcards)
    c['Id'] = c['Id'].format(**wildcards)
    c['SubResources']['@odata.id'] = c['SubResources']['@odata.id'].format(**wildcards)

    c['SerialNumber'] = strgen.StringGenerator('[A-Z]{3}[0-9]{10}').render()

    return c
