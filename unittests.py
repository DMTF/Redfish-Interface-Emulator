#
# Copyright (c) 2016 Intel Corporation. All Rights Reserved.
# Copyright (c) 2016, The Storage Networking Industry Association.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# Neither the name of The Storage Networking Industry Association (SNIA) nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

"""
Python unittests for the Redfish API Emulator
"""
import argparse
import unittest
import requests
import json
import os
import logging
import webbrowser
import sys

class TestRedfishEmulator(unittest.TestCase):
    MODE=None
    #global address
    CONFIG = 'emulator-config.json'
    with open(CONFIG, 'r') as f:
        config = json.load(f)
    
    MODE = config['MODE']
    address = sys.argv[2]
    base_url = 'http://{0}/redfish/v1/'.format(address)
  
    unittest_data = 'unittest_data'
    log_file = None
    log_fmt = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)-8s: %(message)s',
        datefmt='%H:%M:%S %m-%d-%y')

    

    def assert_status(self, r, expected, logger):
        try:
            assert r.status_code == expected, 'Request failed: See log "{0}"'.format(self.log_file)
        except AssertionError:
            # Catching assertion to log the response from the REST server
            # then re-raising the exception
            logger.error('Request Failed:\n' + r.text)
            raise

    def url(self, url):
        """
        Appends the base_url to the beginning of the given URL
        """
        return self.base_url + url

    def odata_id_url(self, url):
        """
        Appends http://<address>/ to the given url
        """
        return 'http://{0}{1}'.format(self.address, url)

    def get(self, logger, url, getting):
        """
        Helper function to do a get request and log it to the specified logger
        """
        r = requests.get(url)
        self.assert_status(r, 200, logger)
	logger.info('PASS: GET of {0} successful (response below)\n {1}'.format(getting, r.text))

    def get_logger(self, name, log_file):
        """
        Helper function to create a logger object
        """
        logger = logging.getLogger(name)
        fh = logging.FileHandler(log_file, mode='w')
        fh.setFormatter(self.log_fmt)
        logger.setLevel(logging.INFO)
        logger.addHandler(fh)
        return logger

    def do_gets(self, params, logger):
        """
        Helper function to call the get() member function with the given params.
        Params must be a list of parameters to give to the get()method.
        """
        for param in params:
            #try:
                self.get(logger, *param)
            #except Exception,e:
            #    print str(e),"Exception *******************"

    def redfish_get_serviceroot(self): #test_redfish_get_serviceroot
        self.log_file = 'test-get-serviceroot.log'
        logger = self.get_logger(
            'test-get-serviceroot',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url(''), 'Service Root')
	]
 
        self.do_gets(params, logger)

    def redfish_get_system(self): #test_redfish_get_system(self):
        """
        Unit test to get resource of a system instance

        NOTE: The emulator must be in the redfish mode to run this test
        """
        self.log_file = 'test-get-system.log'
        logger = self.get_logger(
            'test-get-system',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('Systems/437XR1138R2/'), 'System instance'),
            (self.url('Systems/437XR1138R2/SimpleStorage/'), 'SimpleStorageCollection'),
            (self.url('Systems/437XR1138R2/SimpleStorage/1/'), 'SimpleStorage member 1')]

        self.do_gets(params, logger)

        # Testing deleting the system instance (expect to fail with 404)
        r = requests.delete(self.url('Systems/437XR1138R2/'))
        self.assert_status(r, 404, logger)
	logger.info('PASS: Unable to delete system instance')

#Unit test for the sprint 3
    def test_chasis(self):
        self.log_file = 'testresults_chasis.log'
        logger = self.get_logger(
            'Chassis',
            self.log_file)

        # Parameters for the get requests
        params = [
            #(self.url('Chassis/StorageChassis1/Power/'), 'Power'),
            #(self.url('Chassis/StorageChassis1/Thermal/'), 'Thermal'),


            #(self.url('StorageServices/1/ClassesOfService'), 'Power'),
            #(self.url('Systems/437XR1138R2/SimpleStorage/'), 'SimpleStorageCollection'),
            #(self.url('Systems/437XR1138R2/SimpleStorage/1/'), 'SimpleStorage member 1')
             ]

        self.do_gets(params, logger)


    def test_storage_service(self): #test_storage_service
        self.log_file = 'testresults-storage_services3.log'
        logger = self.get_logger('Storage services', self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('StorageServices/1/ClassesOfService/'), 'ClassesOfService'),
            (self.url('StorageServices/1/ClassesOfService/GoldBoston'), 'GoldBoston'),
            (self.url('StorageServices/1/ClassesOfService/SilverBoston'), 'SilverBoston'),
            (self.url('StorageServices/1/ClassesOfService/GoldProvidence'), 'GoldProvidence'),
            (self.url('StorageServices/1/ClassesOfService/SilverProvidence'), 'SilverProvidence'),
            (self.url('StorageServices/1/ClassesOfService/BostonGoldJaw'), 'BostonGoldJaw'),
            (self.url('StorageServices/1/ClassesOfService/BostonSilverJaw'), 'BostonSilverJaw'),
            (self.url('StorageServices/1/ClassesOfService/BostonBunker'), 'BostonBunker'),
            (self.url('StorageServices/1/ClassesOfService/BostonVMs'), 'BostonVMs'),
         ]

        self.do_gets(params, logger)


    def test_storage_service_2(self): #test_storage_service
        self.log_file = 'testresults-storage_services_2.log'
        logger = self.get_logger(
            'Storage services 2',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('StorageServices/1/ClientEndpointGroups'), 'ClientEndpointGroups'),
            (self.url('StorageServices/1/DataProtectionLoSCapabilities'), 'DataProtectionLoSCapabilities'),
            (self.url('StorageServices/1/DataSecurityLoSCapabilities'), 'DataSecurityLoSCapabilities'),
            (self.url('StorageServices/1/DataStorageLoSCapabilities'), 'DataStorageLoSCapabilities'),
            (self.url('StorageServices/1/Drives'), 'Drives'),
            (self.url('StorageServices/1/Endpoints'), 'Endpoints'),
            (self.url('StorageServices/1/Endpoints/1'), 'Endpoints/1 '),
            (self.url('StorageServices/1/Endpoints/2'), 'Endpoints/2'),

        ]

        #self.do_gets(params, logger)


    def test_storage_service_2(self): #test_storage_service
        self.log_file = 'prasanth_storage_services_2.log'
        logger = self.get_logger(
            'Storage services 2',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('StorageServices/1/ClientEndpointGroups'), 'ClientEndpointGroups'),
            (self.url('StorageServices/1/DataProtectionLoSCapabilities'), 'DataProtectionLoSCapabilities'),
            (self.url('StorageServices/1/DataSecurityLoSCapabilities'), 'DataSecurityLoSCapabilities'),
            (self.url('StorageServices/1/DataStorageLoSCapabilities'), 'DataStorageLoSCapabilities'),
            (self.url('StorageServices/1/Drives'), 'Drives'),
            (self.url('StorageServices/1/Endpoints'), 'Endpoints'),
            (self.url('StorageServices/1/Endpoints/1'), 'Endpoints/1 '),
            (self.url('StorageServices/1/Endpoints/2'), 'Endpoints/2'),

            (self.url('StorageServices/1/IOConnectivityLoSCapabilities'), 'IOConnectivityLoSCapabilities'),
            (self.url('StorageServices/1/IOPerformanceLoSCapabilities'), 'IOPerformanceLoSCapabilities'),
            (self.url('StorageServices/1/ServerEndpointGroups'), 'ServerEndpointGroups'),
            (self.url('StorageServices/1/StorageGroups'), 'StorageGroups'),

            (self.url('StorageServices/1/StorageGroups/1'), 'StorageGroups/1'),
            (self.url('StorageServices/1/StorageGroups/2'), 'StorageGroups/2'),
            (self.url('StorageServices/1/StorageGroups/3'), 'StorageGroups/3'),

            (self.url('StorageServices/1/StoragePools'), 'StoragePools'),
            (self.url('StorageServices/1/StoragePools/BasePool'), 'BasePool'),
            (self.url('StorageServices/1/StoragePools/SpecialPool'), 'SpecialPool'),

        ]

        self.do_gets(params, logger)



    def test_storage_services_volume(self):
        self.log_file = 'testresults-storage_services_volume.log'
        logger = self.get_logger(
            'Storage Services Volume',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('StorageServices/1/Volumes'), 'Volumes'),
            (self.url('StorageServices/1/Volumes/61001234876545676100123487654567'), '61001234876545676100123487654567'),
            (self.url('StorageServices/1/Volumes/65456765456761001234876100123487'), '61001234876545676100123487654567'),
            (self.url('StorageServices/1/Volumes/3'), 'Volumes 3'),
            (self.url('StorageServices/1/Volumes/4'), 'Volumes 4'),
            (self.url('StorageServices/1/Volumes/5'), 'Volumes 5'),
            (self.url('StorageServices/1/Volumes/6'), 'Volumes 6')

            #(self.url('StorageServices/1/ClassesOfService'), 'Power'),
            #(self.url('Systems/437XR1138R2/SimpleStorage/'), 'SimpleStorageCollection'),
            #(self.url('Systems/437XR1138R2/SimpleStorage/1/'), 'SimpleStorage member 1')
             ]

        #self.do_gets(params, logger)


    def test_storage_services_file_service(self):
        self.log_file = 'testresults-storage_file_service.log'
        logger = self.get_logger('Storage Services File Service', self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('StorageServices/FileService/ClassesOfService/Gold'), 'Gold'),
            (self.url('StorageServices/FileService/ClassesOfService/Silver'), 'Silver'),
            (self.url('StorageServices/FileService/ClassesOfService/BostonBunker'), 'BostonBunker'),
            (self.url('StorageServices/FileService/ClassesOfService/BostonGoldJaw'), 'BostonGoldJaw'),
            (self.url('StorageServices/FileService/ClassesOfService/BostonSilverJaw'), 'BostonSilverJaw'),
            (self.url('StorageServices/FileService/ClassesOfService/BostonVMs'), 'BostonVMs'),
            (self.url('StorageServices/FileService/DataProtectionLoSCapabilities'), 'DataProtectionLoSCapabilities'),
            (self.url('StorageServices/FileService/DataSecurityLoSCapabilities'), 'DataSecurityLoSCapabilities'),
            (self.url('StorageServices/FileService/DataStorageLoSCapabilities'), 'DataStorageLoSCapabilities'),
            (self.url('StorageServices/FileService/FileSystems'), 'FileSystems'),
            #(self.url('StorageServices/FileService/FileSystems/FS1'), 'FileSystems/FS1'),
            (self.url('StorageServices/FileService/IOConnectivityLoSCapabilities'), 'IOConnectivityLoSCapabilities'),
            (self.url('StorageServices/FileService/IOPerformanceLoSCapabilities'), 'IOPerformanceLoSCapabilities'),
            (self.url('StorageServices/FileService/StorageGroups'), 'StorageGroups'),

            (self.url('StorageServices/FileService/StorageGroups/1'), 'StorageGroups/1'),
            (
            self.url('StorageServices/FileService/StorageGroups/2'), 'StorageGroups/2'),
            (
            self.url('StorageServices/FileService/StorageGroups/3'), 'StorageGroups/3'),
            (self.url('StorageServices/FileService/StoragePools'), 'StoragePools'),
            (self.url('StorageServices/FileService/StoragePools/BasePool'), 'BasePool'),
            (self.url('StorageServices/FileService/StoragePools/SpecialPool'), 'SpecialPool')
            #(self.url('StorageServices/1/Volumes/6'), 'Volumes 6'),

            #(self.url('StorageServices/1/ClassesOfService'), 'Power'),
            #(self.url('Systems/437XR1138R2/SimpleStorage/'), 'SimpleStorageCollection'),
            #(self.url('Systems/437XR1138R2/SimpleStorage/1/'), 'SimpleStorage member 1')
             ]

        #self.do_gets(params, logger)

    def test_storage_services_simple_1(self):
        self.log_file = 'testresults-storage_simple_1.log'
        logger = self.get_logger(
            'Storage Services Simple 1',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('StorageServices/Simple1/ClientEndpointGroups'), 'ClientEndpointGroups'),
            (self.url('StorageServices/Simple1/Drives'), 'Drives'),
            (self.url('StorageServices/Simple1/Endpoints'), 'Endpoints'),
            (self.url('StorageServices/Simple1/Endpoints/1'), 'Endpoints/1'),
            (self.url('StorageServices/Simple1/Endpoints/2'), 'Endpoints/2'),
            (self.url('StorageServices/Simple1/ServerEndpointGroups'), 'ServerEndpointGroups'),
            (self.url('StorageServices/Simple1/StorageGroups'), 'StorageGroups'),
            (self.url('StorageServices/Simple1/StorageGroups/1'), 'StorageGroups/1'),
            (self.url('StorageServices/Simple1/StorageGroups/2'), 'StorageGroups/2'),
            (self.url('StorageServices/Simple1/StoragePools'), 'StoragePools'),
            (self.url('StorageServices/Simple1/StoragePools/BasePool'), 'BasePool'),
            (self.url('StorageServices/Simple1'), 'Simple1'),
            (self.url('StorageServices/Simple1/Volumes'), 'Volumes'),
            (self.url('StorageServices/Simple1/Volumes/1'), 'Volumes/1'),
            (self.url('StorageServices/Simple1/Volumes/2'), 'Volumes/2'),
            (self.url('StorageServices/Simple1/Volumes/3'), 'Volumes/3'),
            (self.url('StorageServices/Simple1/Volumes/4'), 'Volumes/4'),
             ]

        self.do_gets(params, logger) 
"""
    def test_systems_complx_eth(self):
        self.log_file = 'testresults-systems_complx_eth.log'
        logger = self.get_logger(
            'System Complex Ethernet Results',
            self.log_file)

      # Parameters for the get requests
        params = [
            (self.url('Systems/Complex/EthernetInterfaces'), 'ClientEndpointGroups'),
            (self.url('Systems/Complex/EthernetInterfaces/1'), 'EthernetInterfaces 1'),
            (self.url('Systems/Complex/EthernetInterfaces/1/VLANs'), 'EthernetInterfaces VLANs'),
            (self.url('Systems/Complex/EthernetInterfaces/1/VLANs/1'), 'EthernetInterfaces VLANs 1'),
            (self.url('Systems/Complex/LogServices'), 'LogServices'),
            (self.url('Systems/Complex/LogServices/Log1'), 'LogServices Log 1'),
            (self.url('Systems/Complex/LogServices/Log1/Entries'), 'LogServices Log 1 Entries'),
            (self.url('Systems/Complex/LogServices/Log1/Entries/1'), 'LogServices Log 1 Entries 1'),
            (self.url('Systems/Complex/LogServices/Log1/Entries/2'), 'LogServices Log 1 Entries 2'),

             ]
            
        self.do_gets(params, logger)

    def test_systems_complx_eth(self):
        self.log_file = 'testresults-systems_complx_eth.log'
        logger = self.get_logger(
            'System Complex Ethernet Results',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('Systems/Complex/EthernetInterfaces'), 'ClientEndpointGroups'),
            (self.url('Systems/Complex/EthernetInterfaces/1'), 'EthernetInterfaces 1'),
            (self.url('Systems/Complex/EthernetInterfaces/1/VLANs'), 'EthernetInterfaces VLANs'),
            (self.url('Systems/Complex/EthernetInterfaces/1/VLANs/1'), 'EthernetInterfaces VLANs 1'),
            (self.url('Systems/Complex/LogServices'), 'LogServices'),
            (self.url('Systems/Complex/LogServices/Log1'), 'LogServices Log 1'),
            (self.url('Systems/Complex/LogServices/Log1/Entries'), 'LogServices Log 1 Entries'),
            (self.url('Systems/Complex/LogServices/Log1/Entries/1'), 'LogServices Log 1 Entries 1'),
            (self.url('Systems/Complex/LogServices/Log1/Entries/2'), 'LogServices Log 1 Entries 2'),

             ]

        self.do_gets(params, logger)

    def test_systems_complx_eth(self):
        self.log_file = 'test-sprint_3_testresults-systems_complx_eth.log'
        logger = self.get_logger(
            'System Complex Ethernet Results',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('Systems/Complex/EthernetInterfaces'), 'ClientEndpointGroups'),
            (self.url('Systems/Complex/EthernetInterfaces/1'), 'EthernetInterfaces 1'),
            (self.url('Systems/Complex/EthernetInterfaces/1/VLANs'), 'EthernetInterfaces VLANs'),
            (self.url('Systems/Complex/EthernetInterfaces/1/VLANs/1'), 'EthernetInterfaces VLANs 1'),
            (self.url('Systems/Complex/LogServices'), 'LogServices'),
            (self.url('Systems/Complex/LogServices/Log1'), 'LogServices Log 1'),
            (self.url('Systems/Complex/LogServices/Log1/Entries'), 'LogServices Log 1 Entries'),
            (self.url('Systems/Complex/LogServices/Log1/Entries/1'), 'LogServices Log 1 Entries 1'),
            (self.url('Systems/Complex/LogServices/Log1/Entries/2'), 'LogServices Log 1 Entries 2'),

             ]

        self.do_gets(params, logger)

    def test_systems_proc_stor(self):
        self.log_file = 'test-sprint_3_testresults-systems_proc_stor.log'
        logger = self.get_logger(
            'System Complex Processor StorageServices',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('Systems/Complex/Processors'), 'Processors'),
            (self.url('Systems/Complex/Processors/1'), 'Processors 1'),
            (self.url('Systems/Complex/Processors/2'), 'Processors 2'),
            (self.url('Systems/fileserver/StorageServices'), 'StorageServices'),

             ]

        self.do_gets(params, logger)

    def test_fileserver_complx_eth(self):
        self.log_file = 'test-sprint_3_testresults-fileserver_complx_eth.log'
        logger = self.get_logger(
            'Fileserver Complex Ethernet Results',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('Systems/FileServer/EthernetInterfaces'), 'ClientEndpointGroups'),
            (self.url('Systems/FileServer/EthernetInterfaces/1'), 'EthernetInterfaces 1'),
            (self.url('Systems/FileServer/EthernetInterfaces/1/VLANs'), 'EthernetInterfaces VLANs'),
            (self.url('Systems/FileServer/EthernetInterfaces/1/VLANs/1'), 'EthernetInterfaces VLANs 1'),
            (self.url('Systems/FileServer/LogServices'), 'LogServices'),
            (self.url('Systems/FileServer/LogServices/Log1'), 'LogServices Log 1'),
            (self.url('Systems/FileServer/LogServices/Log1/Entries'), 'LogServices Log 1 Entries'),
            (self.url('Systems/FileServer/LogServices/Log1/Entries/1'), 'LogServices Log 1 Entries 1'),
            (self.url('Systems/FileServer/LogServices/Log1/Entries/2'), 'LogServices Log 1 Entries 2'),

             ]

        self.do_gets(params, logger)

    def test_fileserver_proc_stor(self):
        self.log_file = 'test-sprint_3_testresults-fileserver_proc_stor.log'
        logger = self.get_logger(
            'Fileserver Complex Processor StorageServices',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('Systems/FileServer/Processors'), 'Processors'),
            (self.url('Systems/FileServer/Processors/1'), 'Processors 1'),
            (self.url('Systems/FileServer/Processors/2'), 'Processors 2'),
            (self.url('Systems/FileServer/StorageServices'), 'StorageServices'),
             ]

        self.do_gets(params, logger)

    def test_simple_complx_eth(self):
        self.log_file = 'test-sprint_3_testresults-simple_complx_eth.log'
        logger = self.get_logger(
            'Simple Complex Ethernet Results',
            self.log_file)

        # Parameters for the get requests
        params = [
            #(self.url('Systems/Simple/EthernetInterfaces'), 'ClientEndpointGroups'),
            #(self.url('Systems/Simple/EthernetInterfaces/1'), 'EthernetInterfaces 1'),
            #(self.url('Systems/Simple/EthernetInterfaces/1/VLANs'), 'EthernetInterfaces VLANs'),
            #(self.url('Systems/Simple/EthernetInterfaces/1/VLANs/1'), 'EthernetInterfaces VLANs 1'),
            #(self.url('Systems/Simple/LogServices'), 'LogServices'),
            #(self.url('Systems/Simple/LogServices/Log1'), 'LogServices Log 1'),
            #(self.url('Systems/Simple/LogServices/Log1/Entries'), 'LogServices Log 1 Entries'),
            #(self.url('Systems/Simple/LogServices/Log1/Entries/1'), 'LogServices Log 1 Entries 1'),
            #(self.url('Systems/Simple/LogServices/Log1/Entries/2'), 'LogServices Log 1 Entries 2'),

             ]

        self.do_gets(params, logger)

    def test_simple_proc_stor(self):
        self.log_file = 'test-sprint_3_testresults-simple_proc_stor.log'
        logger = self.get_logger(
            'Simple Complex Processor StorageServices',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('Systems/Simple/Processors'), 'Processors'),
            (self.url('Systems/Simple/Processors/1'), 'Processors 1'),
            (self.url('Systems/Simple/Processors/2'), 'Processors 2'),
            (self.url('Systems/Simple/StorageServices'), 'StorageServices'),
             ]

        self.do_gets(params, logger)

"""
if __name__ == '__main__':
    #main(sys.argv[2:])
    parser = argparse.ArgumentParser()
    parser.add_argument('spec', choices=['Redfish', 'Chinook'], type=str,
                        help='Specification used for pooled node definition'
                             ' by the emulator')
    
    parser.add_argument('address', metavar='address', type=str, nargs=1,
                        help='Address to access the emulator')
    args = parser.parse_args()
    print'Testing interface at:', sys.argv[2]
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRedfishEmulator)
    runner = unittest.TextTestRunner(verbosity=2)

    sub_str = 'chinook'

    if args.spec == 'Chinook':
        sub_str = 'redfish'

    for t in suite:
        if sub_str in t.id():
            setattr(t, 'setUp', lambda: t.skipTest('Emulator running using the {0} spec'.format(args.spec)))
    runner.run(suite)
