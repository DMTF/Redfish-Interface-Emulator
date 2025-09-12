import copy
import logging

_VOLUME_TEMPLATE = {
    "@odata.type": "#Volume.v1_10_1.Volume",
    "Id": "{volume_id}",
    "Name": "Virtual Disk {volume_id}",
    "Status": {
        "State": "Enabled",
        "Health": "OK"
    },
    "Encrypted": False,
    "RAIDType": "{raid_type}",
    "CapacityBytes": "{capacity_bytes}",
    "Identifiers": [
        {
            "DurableNameFormat": "UUID",
            "DurableName": "{durable_name}"
        }
    ],
    "Links": {
        "Drives": []
    },
    "Actions": {
        "#Volume.Initialize": {
            "target": "{rb}Systems/{system_id}/Storage/{storage_id}/Volumes/{volume_id}/Actions/Volume.Initialize",
            "InitializeType@Redfish.AllowableValues": [
                "Fast",
                "Slow"
            ]
        }
    },
    "@odata.id": "{rb}Systems/{system_id}/Storage/{storage_id}/Volumes/{volume_id}"
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

def get_volume_instance(wildcards, drive_ids, raid_type, capacity_bytes):
    """
    Returns a single Volume resource with user-defined RAID type and capacity.

    Args:
        wildcards (dict): Must include rb, system_id, storage_id, volume_id, durable_name
        drive_ids (list): List of drive URIs
        raid_type (str): RAID configuration type
        capacity_bytes (int or str): Volume size in bytes

    Returns:
        dict: Volume resource
    """
    required_keys = ['rb', 'system_id', 'storage_id', 'volume_id', 'durable_name']
    if not all(k in wildcards for k in required_keys):
        raise KeyError(f"Missing required wildcards: {wildcards}")
    
    wildcards["raid_type"] = raid_type
    wildcards["capacity_bytes"] = str(capacity_bytes)
    vol = str(wildcards['volume_id'])
    c = copy.deepcopy(_VOLUME_TEMPLATE)
    c['@odata.id'] = c['@odata.id'].format(rb=wildcards['rb'], system_id=wildcards['system_id'], storage_id=wildcards['storage_id'], volume_id=vol)
    c["Links"]["Drives"] = [{"@odata.id": did} for did in drive_ids]
    replace_recurse(c, wildcards)
    return c
