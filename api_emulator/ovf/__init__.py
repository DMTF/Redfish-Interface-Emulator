# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# OVF Parsers

import re
import xml.etree.ElementTree as ET

# Imports from local Python package
from .namespace import Namespace
from .virtual_system import VirtualSystem

# Imports from rsa_api_emulator
from api_emulator.redfish.simple_storage import Device
from api_emulator.redfish.resource import Status, StateEnum, HealthEnum
from api_emulator.exceptions import OVFParseError

OVF_V2_NS = Namespace(
    {'xmlns': 'http://schemas.dmtf.org/ovf/envelope/2',
     'ovf': 'http://schemas.dmtf.org/ovf/envelope/2',
     'rasd':'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData',
     'vssd': 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData',
     'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
     'vbox': 'http://www.virtualbox.org/ovf/machine',
     'epasd': 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_EthernetPortAllocationSettingData',
     'sasd': 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_StorageAllocationSettingData'})


class SizeUnits(object):
    KB = 'KB'
    MB = 'MB'
    GB = 'GB'
    TB = 'TB'

    @classmethod
    def lt(cls, unit1, unit2):
        """
        Check if unit1 is less than unit2
        """
        cls.assert_valid_unit(unit1)
        cls.assert_valid_unit(unit2)

        if unit1 == cls.KB and unit2 == cls.MB:
            lt = True
        elif unit1 == cls.MB and unit2 == cls.GB:
            lt = True
        elif unit1 == cls.GB and unit2 == cls.TB:
            lt = True
        elif unit1 == cls.MB and unit2 == cls.TB:
            lt = True
        elif unit1 == cls.KB and unit2 == cls.TB:
            lt = True
        elif unit1 == cls.KB and unit2 == cls.GB:
            lt = True
        else:
            lt = False
        return lt


    @classmethod
    def valid_unit(cls, unit):
        valid_units = [cls.KB, cls.MB, cls.GB, cls.TB]
        return unit in valid_units

    @classmethod
    def assert_valid_unit(cls, unit):
        assert cls.valid_unit(unit), 'Invalid Size Unit: ' + unit

    @classmethod
    def convert_to(cls, size, src_unit, dest_unit):
        """
        Returns the number of GB of the given size of MB

        If a non-multiple of 2 is given, then data will be lost, because
        it only does straight multiplication.

        Arguments:
            size - Amount of MB
        """
        cls.assert_valid_unit(src_unit)
        cls.assert_valid_unit(dest_unit)

        op = None

        if src_unit == cls.KB and dest_unit == cls.MB:
            op = lambda x: operator.div(x, 1000)
        elif src_unit == cls.KB and dest_unit == cls.GB:
            op = lambda x: operator.div(x, 1000 * 1024)
        elif src_unit == cls.KB and dest_unit == cls.TB:
            op = lambda x: operator.div(x, 1000 * 1024 * 1000)
        elif src_unit == cls.MB and dest_unit == cls.KB:
            op = lambda x: operator.mul(x, 1000)
        elif src_unit == cls.MB and dest_unit == cls.GB:
            op = lambda x: operator.div(x, 1024)
        elif src_unit == cls.MB and dest_unit == cls.TB:
            op = lambda x: operator.div(x, 1024 * 1000)
        elif src_unit == cls.GB and dest_unit == cls.KB:
            op = lambda x: operator.mul(x, 1000 * 1024)
        elif src_unit == cls.GB and dest_unit == cls.MB:
            op = lambda x: operator.mul(x, 1024)
        elif src_unit == cls.GB and dest_unit == cls.TB:
            op = lambda x: operator.div(x, 1000)
        elif src_unit == cls.TB and dest_unit == cls.KB:
            op = lambda x: operator.mul(x, 1000 * 1024 * 1000)
        elif src_unit == cls.TB and dest_unit == cls.MB:
            op = lambda x: operator.mul(x, 1024 * 1000)
        elif src_unit == cls.TB and dest_unit == cls.GB:
            op = lambda x: operator.mul(x, 1000)

        return op(size)

class ResourceEnum:
    """
    ENUM of ResourceType integers
    """
    PROCESSOR = 3
    MEMORY = 4
    ETHERNET = 10
    DISK = 17
    STORAGE_EXTENT = 19
    LOGICAL_DISK = 31


def get_sizeunits(alloc_units):
    """
    Get the size units from the text specified in an AllocationUnits section
    of an OVF file.
    """
    try:
        units = None
        _, power = alloc_units.split('*')[-1].split('^')
        _bytes = pow(2, int(power))

        if _bytes / (1000 * 1000 * 1024 * 1000):
            units = SizeUnits.TB
        elif _bytes / (1000 * 1000 * 1024):
            units = SizeUnits.GB
        elif _bytes / (1000 * 1000):
            units = SizeUnits.MB
    except ValueError:
        raise OVFParseError(
            ('AllocationUnits incorrectly filled out: value is "{0}", should in '
             'the form "byte*2^<power>"'.format(alloc_units)))
    return units


class Network(object):
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc


class Disk(object):
    """
    OVF Disk Object
    """
    def __init__(self, disk_id, cap, pop_size):
        """
        Disk Constructor
        """
        self.disk_id = disk_id
        self.capacity = cap
        self.populated_size = pop_size

        if pop_size is not None:
            self.populated_size = int(pop_size)


class OVFParser(object):
    """
    OVFParser Class
    """
    def __init__(self, ovf_file):
        """
        OVFParser Constructor

        Arguments:
            ovf_file -- OVF file to parse
        """
        self.ns = Namespace(
            {'rasd':'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ResourceAllocationSettingData',
             'vssd': 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_VirtualSystemSettingData',
             'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
             'vbox': 'http://www.virtualbox.org/ovf/machine',
             'epasd': 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_EthernetPortAllocationSettingData',
             'sasd': 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_StorageAllocationSettingData'})

        self.networks = {}
        self.disks = {}
        self.systems = []

        tree = ET.parse(ovf_file)
        self.root = tree.getroot()
        xmlns = re.findall('(?:{)(.+)(?:}.+)', self.root.tag)[0]

        # Adding OVF version specific prefixes
        self.ns.register_prefixes({'xmlns': xmlns, 'ovf': xmlns})

        try:
            self.ovf_version = int(xmlns.split('/')[-1])
        except ValueError:
            raise OVFParseError(
                'Unable to obtain OVF version from xmlns URL: ' + xmlns)

        try:
            # Must do before parsing the virtual systems:
            #   - Parse the NetworkSection
            #   - Parse the DiskSection
            self._parse_networks()
            self._parse_disk_section()
            self._parse_vss()
        except AssertionError as e:
            raise OVFParseError(e.message)

        # virtual_systems = self.root.findall(self.ns.tag('.//{xmlns}VirtualSystem'))
        # self._parse_vss(virtual_systems)

    def _parse_networks(self):
        """
        Parse all of the networks
        """
        sect = self.root.findall(self.ns.tag('./{xmlns}NetworkSection'))

        if sect:
            sect = sect[0]
            for net in sect.iterfind(self.ns.tag('./{xmlns}Network')):
                name = net.attrib[self.ns.tag('{ovf}name')]
                desc = net.find(self.ns.tag('./{xmlns}Description'))

                if desc is not None:
                    desc = desc.text

                self.networks[name] = Network(name, desc)

    def _parse_disk_section(self):
        """
        Private method to parse the DiskSection
        """
        disks = self.root.findall(self.ns.tag('./{xmlns}DiskSection/{xmlns}Disk'))

        if disks:
            try:
                for d in disks:
                    # print d
                    disk = Disk(d.attrib[self.ns.tag('{ovf}diskId')],
                                int(d.attrib[self.ns.tag('{ovf}capacity')]),
                                d.attrib.get(self.ns.tag('{ovf}populatedSize'), None))
                    # print disk
                    self.disks['ovf:/disk/' + disk.disk_id] = disk
            except KeyError as e:
                key = e.message.split('}')[-1]
                raise OVFParseError('Disk missing attribute: ' + key)
            except ValueError:
                raise OVFParseError(
                    'Incorrectly formed disk, either the capacity '
                    'or the populated size is not an integer')

    def _parse_items(self, vs, system):
        """
        Private method to parse all items from a virtual system
        """
        disk_status = Status(StateEnum.ENABLED, HealthEnum.OK)
        # Getting all StorageItem elements
        storage_items = vs.findall(self.ns.tag('./{xmlns}StorageItem'))
        # Getting all EthernetPortItem elements
        eth_items = vs.findall(self.ns.tag('./{xmlns}EthernetPortItem'))
        # Getting all Item elements
        items = vs.findall(self.ns.tag('./{xmlns}Item'))
        # print items

        # Making sure OVF versions are not being mixed
        assert (storage_items and self.ovf_version == 2) or \
               (not storage_items and self.ovf_version == 1), \
            'OVF types mixed, there should be no StorageItem objects ' \
            'in OVF v1.0'
        assert (eth_items and self.ovf_version == 2) or \
               (not eth_items and self.ovf_version == 1), \
            'OVF types mixed, there should be no StorageItem objects ' \
            'in OVF v1.0'

        # Verifying there are items in associated with the virtual system
        assert items is not None, 'No Item objects in VirtualSystem'

        if storage_items is not None:
            for disk in storage_items:
                size, quantity = self._process_disk(disk, 'sasd')
                for i in range(quantity):
                    idx = len(system.disks) + 1
                    system.disks.append(Device('Disk ' + str(idx), disk_status, size=size))

        if eth_items is not None:
            for eth in eth_items:
                conn = self._process_eth(eth, 'epasd')
                system.network_connections.append(conn)

        try:
            for item in items:
                type_id = item.find(self.ns.tag('./{rasd}ResourceType'))
                assert type_id is not None, 'Missing ResourceType element for Item'
                type_id = int(type_id.text)
                if type_id == ResourceEnum.PROCESSOR:
                    system.proc_type = item.find(self.ns.tag('./{rasd}ResourceSubType'))
                    # assert system.proc_type is not None, 'No ResourceSubType set in the processor Item'
                    if system.proc_type is not None:
                        system.proc_type = system.proc_type.text
                    system.processors = item.find(self.ns.tag('./{rasd}VirtualQuantity'))
                    assert system.processors is not None, 'No VirtualQuantity in the processor Item'
                    system.processors = int(system.processors.text)
                elif type_id == ResourceEnum.DISK or type_id == ResourceEnum.LOGICAL_DISK:
                    assert self.ovf_version == 1, \
                        'OVF versions mixed, there should not be a storage item with tag Item'
                    size, quantity = self._process_disk(item, 'rasd')

                    for i in range(quantity):
                        idx = len(system.disks) + 1
                        system.disks.append(Device('Disk ' + str(idx), disk_status, size=size))
                elif type_id == ResourceEnum.ETHERNET:
                    assert self.ovf_version == 1, \
                        'OVF versions mixed, there should not be an ethernet item with tag Item'
                    conn = self._process_eth(item, 'rasd')
                    system.network_connections.append(conn)
                elif type_id == ResourceEnum.MEMORY:
                    units = item.find(self.ns.tag('./{rasd}AllocationUnits'))
                    assert units is not None, 'No AllocationUnits set in the memory Item'
                    units = get_sizeunits(units.text)
                    assert units is not None, 'Unknown memory AllocationUnits, must be MB, GB, or TB'
                    amount = item.find(self.ns.tag('./{rasd}VirtualQuantity'))
                    assert amount is not None, 'No VirtualQuantity found for memory Item'
                    amount = int(amount.text)

                    # Converting amount to GB if not
                    if units != SizeUnits.MB:
                        amount = SizeUnits.convert_to(amount, units, SizeUnits.MB)

                    system.memory_mb += amount
        except ValueError:
            raise OVFParseError(
                'Either one of the ResourceTypes or VirtualQuantities in the '
                'given OVF is not an integer')
        return system

    def _parse_vss(self):
        """
        Private method to parse all the given virtual systems
        """
        virtual_systems = self.root.findall(self.ns.tag('.//{xmlns}VirtualSystem'))

        for vs in virtual_systems:
            hw_sect = vs.find(self.ns.tag('./{xmlns}VirtualHardwareSection'))
            system = VirtualSystem()
            system = self._parse_items(hw_sect, system)
            self.systems.append(system)

    def _process_eth(self, item, pt):
        """
        Private method to process an ethernet item, independent of OVF
        version. Returns the name of the network to connect the ethernet
        item to. Asserts that the connection name element exists
        """
        conn_name = item.find(self.ns.tag('./{' + pt + '}Connection'))
        assert conn_name is not None, 'No Connection element for ethernet item'
        return conn_name.text

    def _process_disk(self, disk, pt):
        """
        Private method to process a storage item independent of the OVF
        version. Returns the following tuple:
            (Storage GB, Quantity)

        Asserts that the following element exist: -- UPDATE THIS DOCUMENTATION
            - AllocationUnits
            - VirtualQuantity
            - Reservation

        This method processes both Logical and Disk items. If the disk is a
        Disk, then the referenced disk must be in the disk section.
        """
        tag = lambda tag: self.ns.tag('./{' + pt + '}' + tag)
        type_id = disk.find(tag('ResourceType'))
        assert type_id is not None, 'Missing ResourceType element for disk'
        type_id = int(type_id.text)
        quantity = 0
        size = None

        if type_id == ResourceEnum.DISK:
            quantity = 1
            disk_path = disk.find(tag('HostResource'))
            assert disk_path is not None, 'Disk missing HostResource element'
            disk_path = disk_path.text

            try:
                disk = self.disks[disk_path]
                amount = disk.capacity
                amount = SizeUnits.convert_to(amount, SizeUnits.KB, SizeUnits.GB)
                size = '{0} {1}'.format(amount, SizeUnits.GB)
            except KeyError:
                raise OVFParseError('Disk does not exist: ' + disk_path)
        elif type_id == ResourceEnum.LOGICAL_DISK:
            quantity = disk.find(tag('VirtualQuantity'))
            assert quantity is not None, 'Missing VirtualQuantity element for logical disk'
            quantity = int(quantity.text)

            amount = disk.find(tag('Reservation'))
            assert amount is not None, 'Missing Reservation element for logical disk'
            amount = int(amount.text)

            units = disk.find(tag('AllocationUnits'))
            assert units is not None, 'Missing AllocationUnits element for logical disk'
            units = get_sizeunits(units.text)
            assert units is not None, 'Unknown amount of AllocationUnits, must be MB, GB, or TB'

            size = '{0} {1}'.format(amount, units)

        return size, quantity


def parse_ovf(ovf_file):
    """
    Parse OVF file and return a list of VirtualSystems.

    Throws an OVFParseError when an error occurs

    Arguments:
        ovf_file - OVF file to parse
    """
    global OVF_V2_NS
    ns = OVF_V2_NS
    tree = ET.parse(ovf_file)
    root = tree.getroot()
    systems = []
    disk_status = Status(StateEnum.ENABLED, HealthEnum.OK)
    virtual_systems = root.findall(ns.tag('.//{xmlns}VirtualSystem'))

    try:
        assert virtual_systems is not None, 'No VirtualSystems found'
        for vs in virtual_systems:
            system = VirtualSystem()
            system.network_ports = len(vs.findall(ns.tag('.//{xmlns}EthernetPortItem')))

            disks = vs.findall(ns.tag('.//{xmlns}StorageItem'))
            assert disks is not None, 'No StorageItems specified in the VirtualSystem'

            items = vs.findall(ns.tag('.//{xmlns}Item'))
            assert items is not None, 'No Items defined in the VirtualSystem'

            # Processing all disks
            for disk in disks:
                # Checking resource type
                type_id = disk.find(ns.tag('.//{sasd}ResourceType'))
                assert type_id is not None, 'No ResourceType in the StorageItem'
                type_id = int(type_id.text)
                assert type_id == ResourceEnum.LOGICAL_DISK, \
                    'Unknown disk resource type: {0}'.format(type_id)
                quantity = disk.find(ns.tag('.//{sasd}VirtualQuantity'))
                assert quantity is not None, 'No VirtualQuantity found in StorageItem'
                quantity = int(quantity.text)

                amount = disk.find(ns.tag('.//{sasd}Reservation'))
                assert amount is not None, 'No Reservation found in StorageItem'
                amount = int(amount.text)

                units = disk.find(ns.tag('.//{sasd}AllocationUnits'))
                assert units is not None, 'No AllocaltionUnits found in StorageItem'
                units = get_sizeunits(units.text)
                assert units is not None, 'Unknown amount of AllocationUnits, must be MB, GB, or TB'

                size = '{0} {1}'.format(amount, units)

                for i in range(quantity):
                    idx = len(system.disks) + 1
                    system.disks.append(Device('Disk ' + str(idx), disk_status, size=size))

            # Processing Items
            for item in items:
                type_id = item.find(ns.tag('.//{rasd}ResourceType'))
                assert type_id is not None, 'No ResourceType in Item'
                type_id = int(type_id.text)

                if type_id == ResourceEnum.PROCESSOR:
                    system.proc_type = item.find(ns.tag('.//{rasd}ResourceSubType'))
                    assert system.proc_type is not None, 'No ResourceSubType set in the processor Item'
                    system.proc_type = system.proc_type.text
                    system.processors = item.find(ns.tag('.//{rasd}VirtualQuantity'))
                    assert system.processors is not None, 'No VirtualQuantity in the processor Item'
                    system.processors = int(system.processors.text)
                elif type_id == ResourceEnum.MEMORY:
                    units = item.find(ns.tag('.//{rasd}AllocationUnits'))
                    assert units is not None, 'No AllocationUnits set in the memory Item'
                    units = get_sizeunits(units.text)
                    assert units is not None, 'Unknown memory AllocationUnits, must be MB, GB, or TB'
                    amount = item.find(ns.tag('.//{rasd}VirtualQuantity'))
                    assert amount is not None, 'No VirtualQuantity found for memory Item'

                    # Converting amount to GB if not
                    if units != SizeUnits.GB:
                        amount = SizeUnits.convert_to(int(amount.text), units, SizeUnits.GB)

                    system.memory_gb += amount
                else:
                    raise OVFParseError('Unknown ResourceType: ' + str(type_id))
            systems.append(system)
    except AssertionError as e:
        raise OVFParseError(e.message)
    return systems
