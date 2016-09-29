Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# Redfish Interface Emulator
The Redfish Interface Emulator that can emulator a Redfish interface resources as static or dynamically.

Static emulator is accomplish by copy a Redfish mockup in a ./static directory.

Dynamic emulator is accomplished by creating the Python files.  The code for an example resource (EgResource) is available to expedite the creation of dynamic resources.  The example is for a collection/member construct, EgResources/{id}.

The emulator is structure so it can be hosted on a standalone system or multiple instances in a Cloud Foundry.  Note: the cloud foundry method has be successful within a company internal cloud foundry service. It has not be attempted on a public cloud foundry service.

This program is a python27 program.
## Installation and Invocation ##
### Standalone ###
The follow is used to install and execute on a standalone system

* Copy the entire directory tree onto the system of interest
* Install the Python packages listed in requirements.txt. The best way to install packages is dependent of your location's firewall and proxy configuration.
	* Use pip
	* Place the packages in ./dependencies and execute install.py
* From this directory, execute the command "python emulator.py"
### Cloud Foundry ###
The follow is used to invoke the emulator in a cloud foundry.

* Copy the entire directory tree onto the system from which the cloud foundry service is invoked
* From this directory, execute the command "cf push <name>".
	* The invocation will cause the Cloud Foundry to install the packages form requirements.txt file and then execute the command in the Procfile file.
### Command Syntax ###
The emulator is invoke with the following command:

    python emulator.py [-h] [-v] [-port PORT] [-debug]
    -h -- help (gives syntax and usage) 
    -v -- verbose
    -port -- specifies the port number to use
    -debug -- enables debugging (needed to debug flask calls)

### Format of emulator_config.json ###
The emulator reads the emulator_config.json file to configure its behavior.
    
    {
        "MODE": "Local"
		"HTTPS": "Disable",
		"SPEC": "Redfish",
        "TRAYS": [
            "./Resources/Systems/1/index.json"
        ]
    }

* The MODE property specifies port to use. If the value is 'Cloud', the port is assigned by
the cloud foundry. If the value is ‘Local’, the port is assigned the value of the port parameter is the command line or 5000, by default. (e.g. localhost:5000/redfish/v1)
* The HTTPS property specifies whether HTTP or HTTPS will used by the client
* The SPEC property specifies whether the computer system is represented as a Redfish ComputerSystem (SPEC = “Redfish”) or another schema.
* The TRAYS property specifies the path to the resources that will make up the initial resource pools. These simple resource pools are depleted as computer systems are composed. Multiple trays can be specified.

### Copying a mockup ###
The location for the static mockup is in the directory ./api_emulator/redfish/static.  The emulator comes with a copy of an earlier Redfish mockup.  This can be replaced with any new mockup file.

If the new mockup has additional resources off the ServiceRoot, then small modifications need to be made in resource_emulator.py to adds these new resources.
### Creating dynamic resources ###
Resources can be incremental recasted as dynamic, so one can straddle static vs dynamic emulation.  The following outlines the overall process. More complete documentation is in a Word document in the ./doc directory.  An example for the Chassis resource is included in the source code.

1. Create a ./api\_emulator/Redfish/template/chassis.py file
	* The file should contain the same properties as the mockup file for the resource
2. Create a ./api\_emulator/Redfish/chassis\_api.py file
	* There is a single file for both the collection resource and the singleton resources
	* Code the behavior for each HTTP command of interest
3. Edit ./api\_emulator/resource\_emulator.py file
	* Comment out the line which loads the static mockup for the Chassis resource
	* Add the line to add the resource API defined in chassis_api.py

### Testing the Emulator
The command to test the emulator can executed against the emulator running locally or hosted in the cloud.

The following is the general command for running unit test.

    python unittests.py <SPEC> "<PATH>"
	(e.g python unittests.py Redfish "localhost:5000")
    <SPEC> should correspond to the value in emulator-config.json
    <PATH> is the path to use for testing and should be enclosed in double-quotes

Once the command completes, inspect the log file which is produced, “test-rsa-emulator.log”.

