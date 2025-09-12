import copy
import strgen
from api_emulator.utils import replace_recurse
TEMPLATE = \
    {
       "@odata.context": "{rb}$metadata#Systems/{id}/Storage",
       "@odata.type": "#StorageCollection.StorageCollection",
        "Name":"Storage Collection",
        "Members@odata.count":"1",
        "Members":[
                {"@odata.id": "/redfish/v1/Systems/{id}/Storage/Storage-1"},
        ],
        "@odata.id":"/redfish/v1/Systems/{id}/Storage"
    }

def get_Storage_instance(wildcards):
    """
    Creates an instace of TEMPLATE and replace wildcards as specfied
    """
    c = copy.deepcopy(TEMPLATE)
    c['@odata.context'] = wildcards['id']
    replace_recurse(c, wildcards)
    return c 