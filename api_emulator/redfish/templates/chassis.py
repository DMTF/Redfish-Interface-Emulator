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
import strgen

_CHASSIS_TEMPLATE = \
    {
        "@odata.context": "{rb}$metadata#Chassis/Links/Members/$entity",
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
                    "@odata.id": "{rb}Systems/"
                }
            ],
            "ManagedBy": [
                {
                    "@odata.id": "{rb}Managers/1"
                }
            ],
         },
    }


def get_Chassis_template(rest_base, ident):
    """
    Formats the template

    Arguments:
        rest_base - Base URL for the RESTful interface
        indent    - ID of the chassis
    """
    c = copy.deepcopy(_CHASSIS_TEMPLATE)

    c['@odata.context'] = c['@odata.context'].format(rb=rest_base)
    c['@odata.id'] = c['@odata.id'].format(rb=rest_base, id=ident)
    c['Id'] = c['Id'].format(id=ident)
    c['Thermal']['@odata.id'] = c['Thermal']['@odata.id'].format(rb=rest_base, id=ident)
    c['Power']['@odata.id'] = c['Power']['@odata.id'].format(rb=rest_base, id=ident)
    c['Links']['ManagedBy'][0]['@odata.id'] = c['Links']['ManagedBy'][0]['@odata.id'].format(rb=rest_base, id=ident)
    c['Links']['ComputerSystems'][0]['@odata.id']=c['Links']['ComputerSystems'][0]['@odata.id'].format(rb=rest_base)

    c['SerialNumber'] = strgen.StringGenerator('[A-Z]{3}[0-9]{10}').render()

    return c
