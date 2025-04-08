import copy
import logging

_TEMPLATE = {
    "@odata.type": "#Bios.v1_2_3.Bios",
    "@odata.id": "{rb}Systems/{id}/Bios",
    "Id": "Bios",
    "Name": "BIOS Configuration Current Settings",
    "AttributeRegistry": "BiosAttributeRegistryP89.v1_0_0",
    "Attributes": {
        "AdminPhone": "",
        "BootMode": "Uefi",
        "EmbeddedSata": "Raid",
        "NicBoot1": "NetworkBoot",
        "NicBoot2": "Disabled",
        "PowerProfile": "MaxPerf",
        "ProcCoreDisable": 0,
        "ProcHyperthreading": "Enabled",
        "ProcTurboMode": "Enabled",
        "UsbControl": "UsbEnabled"
    },
    "ResetBiosToDefaultsPending": "true",
    "@Redfish.Settings": {
        "@odata.type": "#Settings.v1_4_0.Settings",
        "ETag": "9234ac83b9700123cc32",
        "Messages": [
            {
                "MessageId": "Base.1.0.SettingsFailed",
                "RelatedProperties": [
                    "/Attributes/ProcTurboMode"
                ]
            }
        ],
        "SettingsObject": {
            "@odata.id": "{rb}Systems/{id}/Bios/Settings"
        },
        "Time": "2016-03-07T14:44:30-05:00"
    },
    "Actions": {
        "#Bios.ResetBios": {
            "target": "{rb}Systems/{id}/Bios/Actions/Bios.ResetBios"
        },
        "#Bios.ChangePassword": {
            "target": "{rb}Systems/{id}/Bios/Actions/Bios.ChangePassword"
        }
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


def get_Bios_instance(wildcards):
    """
    Creates an instance of _TEMPLATE and replaces wildcards as specified.
    """

    if 'rb' not in wildcards or 'id' not in wildcards:
        raise KeyError(f"Missing required wildcards: {wildcards}")

    c = copy.deepcopy(_TEMPLATE)

    # Replace known placeholders before recursion
    c['@odata.id'] = c['@odata.id'].format(rb=wildcards['rb'], id=wildcards['id'])
    c['@Redfish.Settings']['SettingsObject']['@odata.id'] = (
        c['@Redfish.Settings']['SettingsObject']['@odata.id'].format(rb=wildcards['rb'], id=wildcards['id'])
    )
    c['Actions']['#Bios.ResetBios']['target'] = (
        c['Actions']['#Bios.ResetBios']['target'].format(rb=wildcards['rb'], id=wildcards['id'])
    )
    c['Actions']['#Bios.ChangePassword']['target'] = (
        c['Actions']['#Bios.ChangePassword']['target'].format(rb=wildcards['rb'], id=wildcards['id'])
    )

    replace_recurse(c, wildcards)
    return c

