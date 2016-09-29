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


REDFISH_TEMPLATE  = {
    "@odata.context": "{rest_base}$metadata#Systems/cs_puid",
    "@odata.id": "{rest_base}Systems/{cs_puid}",
    "@odata.type": '#ComputerSystem.1.0.0.ComputerSystem',
    "Id": None,
    "Name": "WebFrontEnd483",
    
    "SystemType": "Virtual",
    "AssetTag": "Chicago-45Z-2381",
    "Manufacturer": "Redfish Computers",
    "Model": "3500RX",
    "SKU": "8675309",
    "SerialNumber": None,
    
    "PartNumber": "224071-J23",
    "Description": "Web Front End node",
    
    "UUID": None,
    "HostName":"web483",
    "Status": {
        "State": "Enabled",
        "Health": "OK",
        "HealthRollUp": "OK"
    },
    
    "IndicatorLED": "Off",
    "PowerState": "On",
    "Boot": {
        "BootSourceOverrideEnabled": "Once",
        "BootSourceOverrideTarget": "Pxe",
        "BootSourceOverrideTarget@DMTF.AllowableValues": [
            "None",
            "Pxe",
            "Floppy",
            "Cd",
            "Usb",
            "Hdd",
            "BiosSetup",
            "Utilities",
            "Diags",
            "UefiTarget"
        ],
        "UefiTargetBootSourceOverride": "/0x31/0x33/0x01/0x01"
    },
    "Oem":{},
    
    "BiosVersion": "P79 v1.00 (09/20/2013)",
    "Processors": {
        "Count": 8,
        "Model": "Multi-Core Intel(R) Xeon(R) processor 7xxx Series",
        "Status": {
            "State": "Enabled",
            "Health": "OK",
            "HealthRollUp": "OK"
        }
    },
    "Memory": {
        "TotalSystemMemoryGB": 16,
        "Status": {
            "State": "Enabled",
            "Health": "OK",
            "HealthRollUp": "OK"
        }
    },
    "Links": {
        "Chassis": [
            {
                "@odata.id": "/redfish/v1/Chassis/1"
            }
        ],
        "ManagedBy": [
            {
                "@odata.id": "/redfish/v1/Managers/1"
            }
        ],
        
        "Processors": {
            "@odata.id": "/redfish/v1/Systems/{cs_puid}/Processors"
        },
        "EthernetInterfaces": {
            "@odata.id": "/redfish/v1/Systems/{cs_puid}/EthernetInterfaces"
        },
        "SimpleStorage": {
            "@odata.id": "/redfish/v1/Systems/{cs_puid}/SimpleStorage"
        },
        "LogService": {
            "@odata.id": "/redfish/v1/Systems/1/Logs"
        }

        
    },
    "Actions": {
        "#ComputerSystem.Reset": {
            "target": "/redfish/v1/Systems/{cs_puid}/Actions/ComputerSystem.Reset",
            "ResetType@DMTF.AllowableValues": [
                "On",
                "ForceOff",
                "GracefulRestart",
                "ForceRestart",
                "Nmi",
                "GracefulRestart",
                "ForceOn",
                "PushPowerButton"
            ]
        },
        
        "Oem": {
            "http://Contoso.com/Schema/CustomTypes#Contoso.Reset": {
                "target": "/redfish/v1/Systems/1/OEM/Contoso/Actions/Contoso.Reset"
            }
        }
    },

        "Oem": {
            "Contoso": {
            "@odata.type": "http://Contoso.com/Schema#Contoso.ComputerSystem",
            "ProductionLocation": {
                "FacilityName": "PacWest Production Facility",
                "Country": "USA"
            }
        },
       "Chipwise": {
            "@odata.type": "http://Chipwise.com/Schema#Chipwise.ComputerSystem",
            "Style": "Executive"
        }
    }
}
         
    
   





