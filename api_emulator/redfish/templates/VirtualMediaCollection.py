import copy
import logging

_TEMPLATE = {
    "@odata.type": "#VirtualMediaCollection.VirtualMediaCollection",
    "@odata.id": "{rb}Managers/{manager_id}/VirtualMedia",
    "Name": "Virtual Media Services",
    "Description": "Redfish-BMC Virtual Media Service Settings",
    "Members@odata.count": 0,  # This will be updated based on the number of members
    "Members": [],
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


def get_virtual_media_collection_instance(wildcards, member_ids):
    """
    Generates a Virtual Media Collection instance with specified member IDs.

    Args:
        wildcards (dict): Must include 'rb' and 'manager_id'
        member_ids (list): List of virtual media device names like ['Floppy1', 'CD1']

    Returns:
        dict: Fully populated VirtualMediaCollection instance
    """

    if 'rb' not in wildcards or 'manager_id' not in wildcards:
        raise KeyError(f"Missing required wildcards: {wildcards}")

    c = copy.deepcopy(_TEMPLATE)
    c['@odata.id'] = c['@odata.id'].format(rb=wildcards['rb'], manager_id=wildcards['manager_id'])
    c["Members@odata.count"] = len(member_ids)

    # Generate member entries
    for member in member_ids:
        c["Members"].append({
            "@odata.id": f"{wildcards['rb']}Managers/{wildcards['manager_id']}/VirtualMedia/{member}"
        })

    replace_recurse(c, wildcards)

    return c