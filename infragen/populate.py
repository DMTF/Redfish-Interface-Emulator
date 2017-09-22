from api_emulator.redfish.EventService_api import EventServiceAPI, CreateEventService
from api_emulator.redfish.Chassis_api import ChassisCollectionAPI, ChassisAPI, CreateChassis
from api_emulator.redfish.ComputerSystem_api import ComputerSystemCollectionAPI, ComputerSystemAPI, CreateComputerSystem
from api_emulator.redfish.Manager_api import ManagerCollectionAPI, ManagerAPI, CreateManager
from api_emulator.redfish.pcie_switch_api import PCIeSwitchesAPI, PCIeSwitchAPI
from api_emulator.redfish.eg_resource_api import EgResourceCollectionAPI, EgResourceAPI, CreateEgResource
from api_emulator.redfish.power_api import CreatePower
from api_emulator.redfish.thermal_api import CreateThermal
from api_emulator.redfish.ComputerSystem.ResetAction_api import ResetAction_API
from api_emulator.redfish.ComputerSystem.ResetActionInfo_api import ResetActionInfo_API
from api_emulator.redfish.processor import CreateProcessor
from api_emulator.redfish.memory import CreateMemory
import g
import random


def populate(num):
    # populate with some example infrastructure
    for i in xrange(num):
        chassis = 'Chassis-{0}'.format(i + 1)
        compSys = 'System-{0}'.format(i + 1)
        bmc = 'BMC-{0}'.format(i + 1)
        # create chassi
        CreateChassis(resource_class_kwargs={
            'rb': g.rest_base, 'linkSystem': compSys, 'linkMgr': bmc}).put(chassis)
        # create chassi subordinate sustems
        CreatePower(resource_class_kwargs={'rb': g.rest_base, 'ch_id': chassis}).put(chassis)
        CreateThermal(resource_class_kwargs={'rb': g.rest_base, 'ch_id': chassis}).put(chassis)
        # create ComputerSystem
        CreateComputerSystem(resource_class_kwargs={
            'rb': g.rest_base, 'linkChassis': chassis, 'linkMgr': bmc}).put(compSys)
        # subordinates, note that .put does not need to be called here
        ResetAction_API(resource_class_kwargs={'rb': g.rest_base, 'sys_id': compSys})
        ResetActionInfo_API(resource_class_kwargs={'rb': g.rest_base, 'sys_id': compSys})
        CreateProcessor(rb=g.rest_base, suffix='System', processor_id='CPU0', suffix_id=compSys, chassis_id=chassis)
        CreateProcessor(rb=g.rest_base, suffix='System', processor_id='CPU1', suffix_id=compSys, chassis_id=chassis)
        CreateMemory(rb=g.rest_base, suffix='System', memory_id='DRAM1', suffix_id=compSys, chassis_id=chassis)
        CreateMemory(rb=g.rest_base, suffix='System', memory_id='NVRAM1', suffix_id=compSys, chassis_id=chassis,
                     capacitymb=65536, devicetype='DDR4', type='NVDIMM_N', operatingmodes='PMEM')
        # create manager
        CreateManager(resource_class_kwargs={
            'rb': g.rest_base, 'linkSystem': compSys, 'linkChassis': chassis, 'linkInChassis': chassis}).put(bmc)
