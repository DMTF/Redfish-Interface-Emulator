#
# Copyright (c) 2016 Intel Corporation. All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer. 
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# Neither the name of the Distributed Management Task Force (DMTF) nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission
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
            self.get(logger, *param)

    def test_redfish_get_serviceroot(self):
        self.log_file = 'test-get-serviceroot.log'
        logger = self.get_logger(
            'test-get-serviceroot',
            self.log_file)

        # Parameters for the get requests
        params = [
            (self.url(''), 'Service Root')
	]
 
        self.do_gets(params, logger)

    def test_redfish_get_system(self):
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
