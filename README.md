Copyright 2016-2018 Distributed Management Task Force, Inc. All rights reserved.

# Redfish Interface Emulator

The Redfish Interface Emulator that can emulator a Redfish interface resources as static or dynamically.

Static emulator is accomplish by copy a Redfish mockup in a ./static directory.

Dynamic emulator is accomplished by creating the Python files.  The code for an example resource (EgResource) is available to expedite the creation of dynamic resources.  The example is for a collection/member construct, EgResources/{id}.

The emulator is structure so it can be hosted on a standalone system or multiple instances in a Cloud Foundry.  Note: the cloud foundry method has be successful within a company internal cloud foundry service. It has not be attempted on a public cloud foundry service.

This program is a python35 program.

## Installation and Invocation

The emulator can be executed locally or on a cloud foundry.  The later allows you to create multiple instances of the emulator.

### Required Python packages

The required python packages for an environment are listed in ./packageSets folder.  The package set files provide a list of environment in which the python code has successfully executed. The files can be generated with a "pip freeze' command. The files are in 'environments.txt' format, so they can be used with pip to install the enviroment.

* Package sets names prefixed with Env-Local are for local execution
* Package sets names prefixed with Env-Cloud are for cloud foundry executions 

### Standalone

1. Use one of the Env-Local package sets file to install the appropriate python packages

	pip install -r [packageSet]
2. Edit the emulator_config.json file and set 

	"MODE": "Local"
3. Start the emulator
	python emulator.py

### Cloud Foundry

For a cloud foundry, the packages listed in the requirements.txt file will be installed during the invocation.

1. Verify that the files requirements.txt, runtime.txt, and Profile exists in the directory

2. Edit the emulator_config.json file and set

	"MODE": "Cloud"

3. Push the emulator to the foundry.  The 'foundry-app-name' will determine the URL for the Redfish service.

	cf push [foundry-app-name]

### Emulator app flags

The emulator is invoke with the following command:

    python emulator.py [-h] [-v] [-port PORT] [-debug]
    -h -- help (gives syntax and usage) 
    -v -- verbose
    -port -- specifies the port number to use
    -debug -- enables debugging (needed to debug flask calls)

### Format of emulator_config.json

The emulator reads the emulator_config.json file to configure its behavior.
    
    {
        "MODE": "Local"
        "HTTPS": "Disable",
        "SPEC": "Redfish",
        "TRAYS": [
            "./Resources/Systems/1/index.json"
        ]
        "POPULATE": "Emulator"
    }

* The MODE property specifies port to use. If the value is 'Cloud', the port is assigned by the cloud foundry. If the value is ‘Local’, the port is assigned the value of the port parameter is the command line or 5000, by default. (e.g. localhost:5000/redfish/v1)
* The HTTPS property specifies whether HTTP or HTTPS will used by the client
* The SPEC property specifies whether the computer system is represented as a Redfish ComputerSystem (SPEC = “Redfish”) or another schema.
* The TRAYS property specifies the path to the resources that will make up the initial resource pools. These simple resource pools are depleted as computer systems are composed. Multiple trays can be specified.
* The POPULATE property specifies the path to the file used by the INFRAGEN module to populate the Redfish Interface backend. If the file does not exist or if POPULATE is not defined, the emulator will start empty.

### Copying a mockup

The location for the static mockup is in the directory ./api_emulator/redfish/static.  The emulator comes with a copy of an earlier Redfish mockup.  This can be replaced with any new mockup file.

If the new mockup has additional resources off the ServiceRoot, then small modifications need to be made in resource_emulator.py to adds these new resources.

### Creating dynamic resources

Resources can be incremental recasted as dynamic, so one can straddle static vs dynamic emulation.  The following outlines the overall process. More complete documentation is in a Word document in the ./doc directory.  An example for the Chassis resource is included in the source code.

1. Create an API file (e.g. Chassis\_api.py)
    * The file is placed in the ./api\_emulator/Redfish directory
    * The file contain the behavior of each HTTP command, of interest
    * The file contains the API for both the singleton resource and the collection resource (if collection exists)
2. Create a template file (e.g. Chassis.py)
    * The file is placed in ./api\_emulator/Redfish/template directory
    * The file should contain the same properties as the mockup file for the resource
3. Edit ./api\_emulator/resource\_emulator.py file
    * Comment out the line which loads the static mockup for the Chassis resource
    * Add the line to add the resource API defined in chassis_api.py

Code generators for the steps #1 (API file) and #2 (template file) exists in the ./codegen directory.

* Generate API file
    * The following command generates an API file
    * The HTTP commands implemented are GET, PATCH, POST and DELETE
    * If the resource has subordinate resources that need to be instantiated when this resource is instantiated, that code will need to be manually added.
* `codegen_api Chassis <outputdir>`

* Generate template file
    * The following command generates a template file
    * The file uses a index.json file located in the current working directory to drive the creation of the template. (TODO - add the filename as a command line parameter)
    * The file contains a dictionary with the names of Redfish collections and there corresponding wildcard.  This dictionary should be update the keep in sync with Redfish modeling. 
* `codegen_template Chassis <outputdir>`

### INFRAGEN Module

Python module that can be used to populate the Redfish Interface backend with data (Chassi, Systems, Resource Blocks, Resources Zones, Processors, Memory, etc).

To use the module a JSON file needs to be in place describing the infrastructure (an example is provided in 'infragen/populate-config.json').

Moreover, the POPULATE property needs to be set in emulator-config.json. The POPULATE property specifies the path to the json file. If the file does not exist or if POPULATE is not defined, the emulator will start empty.

As part of INFRAGEN, generate_template.py can be used to help a user with the creation of JSON template according to a specific Redfish schema by guiding the user through the schema and asking for input values. This module runs independently of the populate function and from the emulator itself.

### Testing the Emulator

The command to test the emulator can executed against the emulator running locally or hosted in the cloud.

The following is the general command for running unit test.

    python unittests.py <SPEC> "<PATH>"
    (e.g python unittests.py Redfish "localhost:5000")
    <SPEC> should correspond to the value in emulator-config.json
    <PATH> is the path to use for testing and should be enclosed in double-quotes

Once the command completes, inspect the log file which is produced, "test-rsa-emulator.log".

### Browser feature - http://localhost:5000/browse.html

Feature added to make it easier to navigate/show the API.

Ability to compose and delete systems (Composition Service) is also included.
    * Compose: when navigating the browser to /CompositionService/ResourceZones/\<ZONE\>/, a check box appears next to each Resource Block. The user shall select the Resource Blocks he wants to use to compose a system and then press the button "compose" on the top.
    * Delete: navigate the browser to /Systems/\<SYSTEM\>/, if the system is of type "COMPOSED", a "delete" button appears. Just click and the composed system will be deleted.

Screenshots of the browser available in /doc/browser-screenshots.pdf
