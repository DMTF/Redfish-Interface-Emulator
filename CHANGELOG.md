# Change Log

## [1.0.8] - 2019-03-26
- Removed emulator_ssl.py
- Clarified how to use HTTPS
- Fixed properties presented in the ChassisCollection resource

## [1.0.7] - 2019-02-08
- Fixed exception handling with how messages are printed

## [1.0.6] - 2018-08-31
- Fixed how new resources are created via POST to allow for creation from templates as well as composed ComputerSystems

## [1.0.5] - 2018-07-16
- Cleanup of package dependencies
- Fixed problems with behavior of issuing POST to dynamic collections

## [1.0.4] - 2018-06-22
- Fixed handling of PATCH on dynamic resources

## [1.0.3] - 2018-06-01
- Made change so that both static and dynamic URLs do not have a trailing /

## [1.0.2] - 2018-05-04
- Fixed Systems collection to be called "Systems"

## [1.0.1] - 2018-03-02
- Fixed usage of the .values() method to match Python3 expectations

## [1.0.0] - 2018-02-16
- Added fixes for running with Python 3.5
- Added browser feature so a human can more easily navigate the service
- Added Composition Service
- Fixed support for running under Linux
- Added code generators for dynamic files
- Fixed inconsistencies for handling URIs with trailing / characters
- Support for setting of Link object paths
- Made Manager and ComputerSystem dynamic
- Implemented wildcards replacement for subordinate resources
- Fixes for Cloud Foundry execution

## [0.9.3] - 2017-05-21
- Change references from flask.ext.restful to flask_restful, since package is obsolete
- Add example files, eg_resource_api.py and eg_resource.py, showing how dynamic objects are coded.

## [0.9.2] - 2017-03-17
- Fixes to run with Python 3.5

## [0.9.0] - 2016-09-22
- Initial Release
