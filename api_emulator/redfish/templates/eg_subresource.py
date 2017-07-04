# Copyright Notice:
# Copyright 2017 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Example Subordinate resource template
import copy
import strgen

_TEMPLATE = \
    {
        "@odata.context": "{rb}$metadata#EgSubResource.EgSubResource",
        "@odata.type": "#EgSubResource.v1_0_0.EgSubResource",
        "@odata.id": "{rb}EgResources/{eg_id}/EgSubResources/{id}",
        "Id": "{id}",
        "Name": "Name of Example Subordinate Resource",
        "Description": "Example subordinate resource.",
        "Manufacturer": "Redfish Computers",
        "SerialNumber": "888el0456",
        "Version": "2.12",
        "PartNumber": "R889e-J23",
        "Status": {
            "State": "Enabled",
            "Health": "OK"
        }
    }

# not used
def get_EgSubResource_instance(rest_base, ident):
    """
    Formats the template

    Arguments:
        rest_base - Base URL for the RESTful interface
        indent    - ID of the resource
    """
    c = copy.deepcopy(_TEMPLATE)

    c['@odata.context'] = c['@odata.context'].format(rb=rest_base)
    c['@odata.id'] = c['@odata.id'].format(rb=rest_base, id=ident)
    c['Id'] = c['Id'].format(id=ident)

    c['SerialNumber'] = strgen.StringGenerator('[A-Z]{3}[0-9]{10}').render()

    return c

def get_EgSubResource_instance2(wildcards):
    """
    Formats the template

    Arguments:
        wildcard - A dictionary of wildcards strings and their repalcement values
    """
    c = copy.deepcopy(_TEMPLATE)

    c['@odata.context'] = c['@odata.context'].format(**wildcards)
    c['@odata.id'] = c['@odata.id'].format(**wildcards)
    c['Id'] = c['Id'].format(**wildcards)

    c['SerialNumber'] = strgen.StringGenerator('[A-Z]{3}[0-9]{10}').render()

    return c
