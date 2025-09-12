import copy
import strgen
from api_emulator.utils import replace_recurse
TEMPLATE = \
    {
       "@odata.type":"#Drive.v1_21_0.Drive",
       "Id":"{dr_id}",
       "Name":"Drive",
        "Name":"Drive Sample",
        "IndicatorLED":"Lit",
        "Model":"C123",
        "Revision":"100A",
        "Status":{
        "State":"Enabled",
        "Health":"OK"} ,
        "CapacityBytes":899527000064,
        "FailurePredicted":"false",
        "Protocol":"SAS",
        "MediaType":"HDD",
        "Manufacturer":"Contoso",
        "SerialNumber":"1234567",
        "PartNumber":"C123-1111",
        "Identifiers":[
        {
        "DurableNameFormat":"NAA",
        "DurableName":"35D38F11ACEF7BD3"
        }
        ],
        "HotspareType":"None",
        "EncryptionAbility":"SelfEncryptingDrive",
        "EncryptionStatus":"Unlocked",
        "RotationSpeedRPM":15000,
        "BlockSizeBytes":512,
        "CapableSpeedGbs":12,
        "NegotiatedSpeedGbs":12,
        "Links":{
        "Volumes":[
        ]
        } ,
        "Actions":{
        "#Drive.SecureErase":{
        "target":"/redfish/v1/Chassis/{ch_id}/Drives/{dr_id}/Actions/Drive.SecureErase"}
        } ,
        "@odata.id":"/redfish/v1/Chassis/{ch_id}/Drives/{dr_id}"
            }

def get_Drive_instance(wildcards):
    """
    Creates an instace of TEMPLATE and replace wildcards as specfied
    """
    c = copy.deepcopy(TEMPLATE)
    c['Id'] = wildcards['dr_id']
    c['Actions']['#Drive.SecureErase']['target'] = c['Actions']['#Drive.SecureErase']['target'].format(**wildcards)
    c['@odata.id']=c['@odata.id'].format(**wildcards)
    #replace_recurse(c, wildcards)
    return c 