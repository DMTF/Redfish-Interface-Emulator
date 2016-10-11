# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

SD_temp={
    "@odata.context": "{rb}$metadata#Managers/Links/Members/1/Links/NICs/Links/Members/1/Links/Settings/$entity",
    "@odata.id": "{rb}Managers/Manager_1/NICs/NIC_1/SD",
    "@odata.type": "#EthernetNetworkInterface.1.00.0.EthernetNetworkInterface",
    "Name": "Manager NIC",
    "Description": "Management Network Interface",
    "FactoryMacAddress": "AA:BB:CC:DD:EE:FF",
    "MacAddress": "AA:BB:CC:DD:EE:FF",
    "LinkTechnology": "Ethernet",
    "SpeedMbps": 100,
    "Autosense": "true",
    "FullDuplex": "true",
    "FrameSize": 1500,
    "HostName": "MyHostName",
    "FQDN": "MyHostName.MyDomainName.com",
    "MaxIPv6StaticAddresses": 1,
    "VLANEnable": "true",
    "VLANId": 101,
    "IPv4Addresses": [
        {
            "Address": "192.168.0.10",
            "SubnetMask": "255.255.252.0",
            "AddressOrigin": "DHCP",
            "Gateway": "192.168.0.1",
            "Oem": {}
        }
    ],
    "IPv6AddressPolicyTable": [
        {
            "Prefix": "::1/128",
            "Precedence": 50,
            "Label": 0
        }
    ],
    "IPv6StaticAddresses": [
        {
            "Address": "fe80::1ec1:deff:fe6f:1e24",
            "PrefixLength": 16
        }
    ],
    "IPv6DefaultGateway": "fe80::1ec1:deff:fe6f:1e24",
    "IPv6Addresses": [
        {
            "Address": "fe80::1ec1:deff:fe6f:1e24",
            "PrefixLength": 64,
            "AddressOrigin": "SLAAC",
            "AddressState": "Preferred",
            "Oem": {}
        }
    ],
    "NameServers": [
        "TheNameServer"
    ],
    "Oem": {}
}


def get_SD_template(rest_base):
    c=SD_temp.copy()
    c['@odata.context']=c['@odata.context'].format(rb=rest_base)
    c['@odata.id']=c['@odata.id'].format(rb=rest_base)
    return c
