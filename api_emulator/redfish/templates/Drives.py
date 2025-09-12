import copy
import strgen
from api_emulator.utils import replace_recurse
TEMPLATE = \
    {
       "@odata.context": "{rb}$metadata#Chassis/{ch_id}/Drives",
       "@odata.type":"#DriveCollection.DriveCollection",
        "Name":"Drive Collection",
        "Members@odata.count":"6",
        "Members":[
                {"@odata.id": "{rb}Chassis/{ch_id}/Drives/Drive-1"},
                {"@odata.id": "{rb}Chassis/{ch_id}/Drives/Drive-2"},
                {"@odata.id": "{rb}Chassis/{ch_id}/Drives/Drive-3"},
                {"@odata.id": "{rb}Chassis/{ch_id}/Drives/Drive-4"},
                {"@odata.id": "{rb}Chassis/{ch_id}/Drives/Drive-5"},
                {"@odata.id": "{rb}Chassis/{ch_id}/Drives/Drive-6"},     
        ]
    }

def get_Drives_instance(wildcards):
    """
    Creates an instace of TEMPLATE and replace wildcards as specfied
    """
    c = copy.deepcopy(TEMPLATE)
    c['@odata.context'] = wildcards['ch_id']
    replace_recurse(c, wildcards)
    return c 