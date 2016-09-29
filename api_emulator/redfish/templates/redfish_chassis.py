#
# Copyright (c) 2016 Intel Corporation. All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# Neither the name of the Distributed Management Task Force (DMTF) nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

"""
Redfish Chassis Template
"""
#from api_emulator.utils import timestamp

_CHASSIS_TEMPLATE = \
    {
        "@odata.context": "{rb}$metadata#Chassis/Links/Members/$entity",
        "@odata.id": "{rb}Chassis/{id}",
        "@odata.type": "#Chassis.1.0.0.Chassis",
        #"Id": None,
        "Name": "Computer System Chassis",
        #"Modified": None,
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
            "ThermalMetrics": {
                "@odata.id": "{rb}Chassis/{id}/ThermalMetrics"
            },
            "PowerMetrics": {
                "@odata.id": "{rb}Chassis/{id}/PowerMetrics"
            },
            "MiscMetrics": {
                "@odata.id": "{rb}Chassis/{id}/MiscMetrics"
            },
            "Oem": {}
        },
        "Oem": {}
    }


def get_chassis_template(rest_base, ident):
    """
    Formats the template

    Arguments:
        rest_base - Base URL for the RESTful interface
        indent    - ID of the chassis
    """
    c = _CHASSIS_TEMPLATE.copy()

    # Formatting
    #c['Id'] = ident
    #c['Modified'] = timestamp()
    c['@odata.context'] = c['@odata.context'].format(rb=rest_base)
    c['@odata.id'] = c['@odata.id'].format(rb=rest_base, id=ident)
    c['Links']['ManagedBy'][0]['@odata.id'] = c['Links']['ManagedBy'][0]['@odata.id'].format(rb=rest_base)
    c['Links']['ThermalMetrics']['@odata.id'] = c['Links']['ThermalMetrics']['@odata.id'].format(rb=rest_base, id=ident)
    c['Links']['PowerMetrics']['@odata.id'] = c['Links']['PowerMetrics']['@odata.id'].format(rb=rest_base, id=ident)
    c['Links']['MiscMetrics']['@odata.id'] = c['Links']['MiscMetrics']['@odata.id'].format(rb=rest_base, id=ident)
    c['Links']['ComputerSystems'][0]['@odata.id']=c['Links']['ComputerSystems'][0]['@odata.id'].format(rb=rest_base)
    return c
