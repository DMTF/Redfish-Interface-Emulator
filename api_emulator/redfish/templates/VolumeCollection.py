import copy
import logging

_VOLUME_COLLECTION_TEMPLATE = {
    "@odata.type": "#VolumeCollection.VolumeCollection",
    "Name": "Storage Volume Collection",
    "Description": "Storage Volume Collection",
    "Members@odata.count": 0,
    "Members": [],
    "@odata.id": "{rb}Systems/{system_id}/Storage/{storage_id}/Volumes"
}

def replace_recurse(c, wildcards):
    """
    Recursively replaces placeholders in dictionaries and lists using the provided wildcards.
    """
    if isinstance(c, dict):
        for k, v in c.items():
            if isinstance(v, str):
                try:
                    c[k] = v.format(**wildcards)
                except KeyError as e:
                    logging.warning(f"Missing wildcard {e} in {k}: {v}")
            else:
                replace_recurse(v, wildcards)
    elif isinstance(c, list):
        for i in range(len(c)):
            replace_recurse(c[i], wildcards)

def get_volume_collection_instance(wildcards, volume_ids):
    """
    Returns a Volume Collection resource with the specified volume member links.

    Args:
        wildcards (dict): Must include 'rb', 'system_id', 'storage_id'
        volume_ids (list): List of volume member IDs (e.g., ['1', '2', '3'])

    Returns:
        dict: Volume Collection resource
    """
    if not all(k in wildcards for k in ['rb', 'system_id', 'storage_id']):
        raise KeyError(f"Missing required wildcards: {wildcards}")

    c = copy.deepcopy(_VOLUME_COLLECTION_TEMPLATE)
    c['@odata.id'] = c['@odata.id'].format(rb=wildcards['rb'], system_id=wildcards['system_id'], storage_id=wildcards['storage_id'])
    c["Members@odata.count"] = len(volume_ids)
    
    c["Members"] = [
        {"@odata.id": f"{wildcards['rb']}Systems/{wildcards['system_id']}/Storage/{wildcards['storage_id']}/Volumes/{vid}"}
        for vid in volume_ids
    ]
    replace_recurse(c, wildcards)
    return c
