# Copyright Notice:
# Copyright 2017 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/master/LICENSE.md

# Example Resoruce Template
import copy
import strgen

_TEMPLATE = \
{
    "@Redfish.Copyright":"Copyright 2014-2016 Distributed Management Task Force, Inc. (DMTF). All rights reserved.",
    "@odata.context": "{rb}$metadata#EventDestination.EventDestination",
    "@odata.id": "{rb}EventService/Subscriptions/{id}",
    "@odata.type": "#EventDestination.v1_0_0.EventDestination",
    "Id": "{id}",
    "Name": "EventSubscription {id}",
    "Destination": "http://www.dnsname.com/Destination{id}",
    "EventTypes": [
        "Alert"
    ],
    "Context": "ABCDEFGHJLKJ",
    "Protocol": "Redfish"
}

def get_Subscription_instance(wildcards):
    """
    Instantiate and format the template

    Arguments:
        wildcard - A dictionary of wildcards strings and their repalcement values

    """
    c = copy.deepcopy(_TEMPLATE)

    c['@odata.context'] = c['@odata.context'].format(**wildcards)
    c['@odata.id'] = c['@odata.id'].format(**wildcards)
    c['Id'] = c['Id'].format(**wildcards)
    c['Destination'] = c['Destination'].format(**wildcards)
    c['Name'] = c['Name'].format(**wildcards)

    return c
