import copy
import logging

# BIOS Settings Template
_BIOS_SETTINGS_TEMPLATE = {
    "@odata.type": "#Bios.v1_2_3.Bios",
    "@odata.id": "{rb}Systems/{id}/Bios/Settings",
    "Id": "Settings",
    "Name": "BIOS Configuration Pending Settings",
    "AttributeRegistry": "BiosAttributeRegistryP89.v1_0_0",
    "Attributes": {
        "AdminPhone": "(404) 555-1212",
        "BootMode": "Uefi",
        "EmbeddedSata": "Ahci",
        "NicBoot1": "NetworkBoot",
        "NicBoot2": "NetworkBoot",
        "PowerProfile": "MaxPerf",
        "ProcCoreDisable": 0,
        "ProcHyperthreading": "Enabled",
        "ProcTurboMode": "Disabled",
        "UsbControl": "UsbEnabled"
    }
}

def replace_recurse(c, wildcards):
    """
    Recursively replaces placeholders in dictionaries and lists using the provided wildcards.
    """
    if isinstance(c, dict):
        for k, v in c.items():
            if isinstance(v, str):  # Replace string values
                try:
                    c[k] = v.format(**wildcards)
                except KeyError as e:
                    logging.warning(f"Missing wildcard {e} in {k}: {v}")
            else:
                replace_recurse(v, wildcards)
    elif isinstance(c, list):
        for i in range(len(c)):
            replace_recurse(c[i], wildcards)

def get_Bios_Settings_instance(wildcards):
    """
    Creates an instance of BIOS Settings and replaces wildcards as needed.
    """
    logging.debug(f"Wildcards: {wildcards}")

    if 'rb' not in wildcards or 'id' not in wildcards:
        raise KeyError(f"Missing required wildcards: {wildcards}")

    c = copy.deepcopy(_BIOS_SETTINGS_TEMPLATE)

    # Replace known placeholders
    c['@odata.id'] = c['@odata.id'].format(rb=wildcards['rb'], id=wildcards['id'])
    replace_recurse(c, wildcards)
    return c