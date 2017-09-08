# Change Log

## [1.0.0] - 2017-09-08
- Fixes for Cloud Foundry execution; Buildpack 1.5.18 supports python 3.5.2
- Implement wildcards replacement for subordinate resources
- Support wildcards in Link object paths
- Make Manager and ComputerSystem dynamic
- By default, instantiate a member for Managers, Chassis and ComputerSystems collections
- Use only flask-restful constructs (remove remnants of flask constructs)
- Added ComputerSystems/{id}/ResetActionInfo and ResetAction resources
- Fixed misspelled module and a few runtime errors and warnings
- Removed trailing / in resource URIs
- Added code generators for dynamic files
- Fixes for running under Linux

## [0.9.2] - 2017-05-21
- Change references from flask.ext.restful to flask_restful, since package is obsolete
- Add example files, eg_resource_api.py and eg_resource.py, showing how dynamic objects are coded.

## [0.9.1] - 2016-03-17
- Fixes to run with Python 3.5

## [0.9.0] - 2016-09-22
- Initial Release
