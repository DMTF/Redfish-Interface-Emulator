from api_emulator.redfish.EventService_api import EventServiceAPI, CreateEventService
from api_emulator.redfish.Chassis_api import ChassisCollectionAPI, ChassisAPI, CreateChassis
from api_emulator.redfish.ComputerSystem_api import ComputerSystemCollectionAPI, ComputerSystemAPI, CreateComputerSystem
from api_emulator.redfish.Manager_api import ManagerCollectionAPI, ManagerAPI, CreateManager
from api_emulator.redfish.pcie_switch_api import PCIeSwitchesAPI, PCIeSwitchAPI
from api_emulator.redfish.eg_resource_api import EgResourceCollectionAPI, EgResourceAPI, CreateEgResource
import g


def infragen(num):

    for i in xrange(num):

        config = CreateChassis()
        out = config.__init__(resource_class_kwargs={'rb': g.rest_base, 'linkSystem': "CS-%d"%i, 'linkMgr': "BMC-%d"%i} )
        out = config.put("Chassis-%d"%i)

        config = CreateComputerSystem()
        out = config.__init__(resource_class_kwargs={'rb': g.rest_base, 'linkChassis': "Chassis-%d"%i, 'linkMgr': "BMC-%d"%i})
        out = config.put("CS-%d"%i)

        config = CreateManager()
        out = config.__init__(resource_class_kwargs={'rb': g.rest_base, 'linkSystem': "CS-%d"%i, 'linkChassis': "Chassis-%d"%i, 'linkInChassis': "Chassis-%d"%i})
        out = config.put("BMC-%d"%i)

