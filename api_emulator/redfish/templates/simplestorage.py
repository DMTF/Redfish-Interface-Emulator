# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md


from copy import deepcopy

_TEMPLATE = {u'@odata.context': '{rb}$metadata#SimpleStorage.SimpleStorage',
             u'@odata.id': "{rb}{suffix}/{suffix_id}/SimpleStorage/{storage_id}",
             u'@odata.type': u'#SimpleStorage.v1_2_0.SimpleStorage',
             u'Description': 'Simple Storage',
             u'Devices': [],
             u'Id': '{storage_id}',
             u'Links': {u'Chassis': {'@odata.id': '{rb}Chassis/{chassis_id}'}},
             u'Name': 'Simple Storage',
             u'Status': {'State': {'Health': 'OK', 'State': 'Enabled'}},
             u'UefiDevicePath': 'Acpi(PNP0A03,0)/Pci(1F|1)/Ata(Primary,Master)/HD(Part3,'
                                ' Sig000101010111100001111011100101100011100000101101100'
                                '1000001000100010101111011001110111100111011010100011111'
                                '0100010101000010111011)'}

_DEVICE_TEMPLATE = {u'CapacityBytes': 550292684800,
                    u'Manufacturer': 'Generic',
                    u'Model': 'Generic',
                    u'Name': 'Generic Storage Device',
                    u'Status': {'State': {'Health': 'OK', 'State': 'Enabled'}}}


def format_storage_template(**kwargs):
    """
    Format the processor template -- returns the template
    """
    # params:
    defaults = {'rb': '/redfish/v1/',
                'suffix': 'Systems',
                'capacitygb': 512,
                'drives': 1}

    defaults.update(kwargs)

    c = deepcopy(_TEMPLATE)
    c['@odata.context'] = c['@odata.context'].format(**defaults)
    c['@odata.id'] = c['@odata.id'].format(**defaults)
    c['Id'] = c['Id'].format(**defaults)
    c['Links']['Chassis']['@odata.id'] = c['Links']['Chassis']['@odata.id'].format(**defaults)
    drives = []
    for i in xrange(defaults['drives']):
        drive = deepcopy(_DEVICE_TEMPLATE)
        drive['CapacityBytes'] = defaults['capacitygb'] * 1024 ** 3
        drive['Name'] = 'Disk %d' % i
        drives.append(drive)
    c['Devices'] = drives
    return c
