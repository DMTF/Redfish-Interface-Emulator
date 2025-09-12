import copy
import logging

_TEMPLATE = {
    "@odata.type": "#VirtualMedia.v1_6_0.VirtualMedia",
    "@odata.id": "{rb}Managers/{manager_id}/VirtualMedia/{member_id}",
    "Id": "{member_id}",
    "Name": "Virtual Media {member_id}",
    "Description": "Represents a virtual media device for remote mounting",
    "Inserted": False,
    "Image": None,
    "MediaTypes": ["CD", "DVD", "Floppy", "USBStick"],
    "WriteProtected": True,
    "ConnectedVia": "NotConnected",
    "TransferMethod": None,
    "TransferProtocolType": None,
    "VerifyCertificate": False,
    "UserName": None,
    "Password": None,
    "ImageName": None,
    "Oem": {},
    "Status": {
        "State": "Enabled",
        "Health": "OK"
    }
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

def get_virtual_media_instance(wildcards):
    """
    Returns a single Virtual Media resource.

    Args:
        wildcards (dict): Must include 'rb', 'manager_id', 'member_id'

    Returns:
        dict: Virtual Media resource
    """
    if not all(k in wildcards for k in ['rb', 'manager_id', 'member_id']):
        raise KeyError(f"Missing required wildcards: {wildcards}")

    c = copy.deepcopy(_TEMPLATE)
    replace_recurse(c, wildcards)
    return c