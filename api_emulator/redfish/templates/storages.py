import copy
import strgen
from api_emulator.utils import replace_recurse

TEMPLATE = \
    {
        "@odata.type": "#Storage.v1_18_0.Storage",
        "Id": "1",
        "Name": "Local Storage Collector",
        "Description": "Integrated RAID Controller",
        "Status": {
            "State": "Enabled",
            "Health": "OK",
            "HealthRollup": "OK"
        },
        "StorageControllers": 
            {
                "@odata.id": "/redfish/v1/Systems/{id}/Storage/Storage-1/StorageControllers/0",
                "MemberId": "0",
                "Name": "HPE Smart Array Controller",
                "Status": {
                    "State": "Enabled",
                    "Health": "OK"
                },
                "Identifiers": [
                    {
                        "DurableNameFormat": "NAA",
                        "DurableName": "345C59DBD970859C"
                    }
                ],
                "Manufacturer": "HPE",
                "Model": "Smart Array P408i-a SR Gen10",
                "SerialNumber": "MXL1234567",
                "PartNumber": "875241-B21",
                "SpeedGbps": 12,
                "FirmwareVersion": "3.56",
                "SupportedControllerProtocols": [
                    "PCIe"
                ],
                "SupportedDeviceProtocols": [
                    "SAS",
                    "SATA"
                ],
                "CacheSummary": {
                    "TotalCacheSizeMiB": 1024,
                    "PersistentCacheSizeMiB": 1024,
                    "Status": {
                        "State": "Enabled",
                        "Health": "OK"
                    }
                }
            },
        
        "Drives":[
            {"@odata.id": "/redfish/v1/Chassis/{ch_id}/Drives/Drive-1"},
            {"@odata.id": "/redfish/v1/Chassis/{ch_id}/Drives/Drive-2"},
            {"@odata.id": "/redfish/v1/Chassis/{ch_id}/Drives/Drive-3"},
            {"@odata.id": "/redfish/v1/Chassis/{ch_id}/Drives/Drive-4"},
            {"@odata.id": "/redfish/v1/Chassis/{ch_id}/Drives/Drive-5"},
            {"@odata.id": "/redfish/v1/Chassis/{ch_id}/Drives/Drive-6"},
            
        ],
        "Volumes":
            {
                "@odata.id":"/redfish/v1/Systems/{id}/Storage/Storage-1/Volumes"
        },
        "Actions":{
        "#Storage.SetEncryptionKey":{
        "target":"/redfish/v1/Systems/{id}/Storage/Storage-1/Actions/Storage.SetEncryptionKey"}
        } ,
        "@odata.id":"/redfish/v1/Systems/{id}/Storage/Storage-1"
    }
        
    
def get_Storages_instance(wildcards):
    """
    Creates an instance of TEMPLATE and replaces wildcards as specified.
    """
    c = copy.deepcopy(TEMPLATE)
    id=wildcards['id']
    ch_id=wildcards['ch_id']
    c['StorageControllers']['@odata.id'] = c['StorageControllers']['@odata.id'].format(**wildcards)
    for i in range(len(c["Drives"])):
        c["Drives"][i]["@odata.id"] = c["Drives"][i]["@odata.id"].format(**wildcards)
    c["Volumes"]["@odata.id"] = c["Volumes"]["@odata.id"].format(**wildcards)
    c["Actions"]["#Storage.SetEncryptionKey"]["target"] = c["Actions"]["#Storage.SetEncryptionKey"]["target"].format(**wildcards)
    c["@odata.id"]=c["@odata.id"].format(**wildcards)
    return c
