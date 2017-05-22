# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

import copy

Statistics_TEMPLATE={
    "@odata.context": "{rb}$metadata#ietf_interfaces.interfaces_state.statistics.statistics",
    "@odata.type": "#ietf_interfaces.interfaces_state.statistics.v1_0_0.statistics",
    "@odata.id": "{rb}NetworkDevices/{sw_id}/ietf_interfaces/interfaces_state/{if_state_id}/statistics",
    "Id": "statistics",
    "Name": "Statistics for interfaces",
    "discontinuity_time": "2016-04-16T11:15.11+05:30",
    "in_octets": 654321,
    "in_unicast_pkts": 600000,
    "in_broadcast_pkts": 50000,
    "in_multicast_pkts": 4000,
    "in_discards": 300,
    "in_errors": 20,
    "in_unknown_protos": 1
}


def create_Statistics_instance(rest_base,sw_id,if_state_id):

    c = copy.deepcopy(Statistics_TEMPLATE)

    c['@odata.context']=c['@odata.context'].format(rb=rest_base)
    c['@odata.id']=c['@odata.id'].format(rb=rest_base,sw_id=sw_id,if_state_id=if_state_id)

    return c
