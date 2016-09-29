#-----------------------------------------------------------------------------
# INTEL CONFIDENTIAL
# Copyright 2015 Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related to
# the source code ("Material") are owned by Intel Corporation or its suppliers
# or licensors. Title to the Material remains with Intel Corporation or its
# suppliers and licensors. The Material contains trade secrets and proprietary
# and confidential information of Intel or its suppliers and licensors. The
# Material is protected by worldwide copyright and trade secret laws and
# treaty provisions. No part of the Material may be used, copied, reproduced,
# modified, published, uploaded, posted, transmitted, distributed, or
# disclosed in any way without Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be
# express and approved by Intel in writing.
#-----------------------------------------------------------------------------
import copy

PCIePort_TEMPLATE={
    "@odata.context": "{rb}$metadata#PCIeSwitches/Members/{sw_id}/Ports/Members$entity",
    "@odata.type": "PCIePort.v1_0_0.PCIePort",
    "@odata.id": "{rb}PCIeSwitches/{sw_id}/Ports/{id}",
 
    "Id": "{id}",
    "Name": "PCIe Port",
    "Description": "PCIe port",
    "PortType": "Upstream",
    "PhysicalPort": "TRUE",

    "PortId": "2",
    "SpeedGBps": 4,
    "Width": 4,
    "MaxSpeedGBps": 8,
    "MaxWidth": 8,

    "OperationalState": "Up",
    "AdministrativeState": "Up",
    "Status": {
        "State": "Enabled",
        "Health": "OK"
    },
    
    "Actions": {
        "#PCIePort.SetState": {
            "target": "{rb}PCIeSwitches/{sw_id}/Ports/{id}/Actions/Port.SetState",
            "SetStateType@Redfish.AllowableValues": [
                "Up",
                "Down",
            ]
    },
}
    }


def get_PCIePort_template(rest_base,sw_id,ident):

    c = copy.deepcopy(PCIePort_TEMPLATE)

    c['@odata.context']=c['@odata.context'].format(rb=rest_base,sw_id=sw_id)
    c['@odata.id']=c['@odata.id'].format(rb=rest_base,sw_id=sw_id,id=ident)
    c['Id'] = c['Id'].format(id=ident)
    c['Actions']['#PCIePort.SetState']['target']=c['Actions']['#PCIePort.SetState']['target'].format(rb=rest_base,sw_id=sw_id,id=ident)

    return c
