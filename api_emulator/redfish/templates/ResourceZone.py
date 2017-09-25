# Copyright Notice:
# Copyright 2017 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Example Resource Zone Template
import copy
import strgen

_TEMPLATE = \
{
    "@Redfish.Copyright": "Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
    "@odata.context": "{rb}$metadata#Zone.Zone",
    "@odata.id": "{rb}CompositionService/ResourceZones/{id}",
    "@odata.type": "#Zone.v1_1_0.Zone",
    "Id": "{id}",
    "Name": "Resource Zone",
    "Status": {
            "State": "Enabled",
            "Health": "OK"
        },
    "Links": {
            "ResourceBlocks": [
                {
                    "@odata.id": "{rb}CompositionService/ResourceBlocks/{linkBlock}"
                }
            ],
         },
    "@Redfish.CollectionCapabilities": {
            "MISSING": "MISSING"
         },

}


def get_ResourceZone_instance(wildcards):
    """
    Instantiate and format the template

    Arguments:
        wildcard - A dictionary of wildcards strings and their replacement values

    """
    c = copy.deepcopy(_TEMPLATE)

    c['@odata.context'] = c['@odata.context'].format(**wildcards)
    c['@odata.id'] = c['@odata.id'].format(**wildcards)
    c['Id'] = c['Id'].format(**wildcards)

    # c['Processors']['@odata.id'] = c['Processors']['@odata.id'].format(**wildcards)
    # c['Memory']['@odata.id'] = c['Memory']['@odata.id'].format(**wildcards)
    # c['EthernetInterfaces']['@odata.id'] = c['EthernetInterfaces']['@odata.id'].format(**wildcards)
    # c['NetworkInterfaces']['@odata.id'] = c['NetworkInterfaces']['@odata.id'].format(**wildcards)
    # c['SimpleStorage']['@odata.id'] = c['SimpleStorage']['@odata.id'].format(**wildcards)
    #
    #c['Links']['ComputerSystems'][0]['@odata.id'] = c['Links']['ComputerSystems'][0]['@odata.id'].format(**wildcards)
    #c['Links']['Chassis'][0]['@odata.id'] = c['Links']['Chassis'][0]['@odata.id'].format(**wildcards)
    c['Links']['ResourceBlocks'][0]['@odata.id'] = c['Links']['ResourceBlocks'][0]['@odata.id'].format(**wildcards)
    #
    # c['Actions']['#ComputerSystem.Reset']['target'] = c['Actions']['#ComputerSystem.Reset']['target'].format(**wildcards)
    # c['Actions']['#ComputerSystem.Reset']['@Redfish.ActionInfo'] = c['Actions']['#ComputerSystem.Reset']['@Redfish.ActionInfo'].format(**wildcards)

    return c
