Copyright 2016-2019 DMTF. All rights reserved.

# Redfish Interface Emulator

The Redfish Interface Emulator that can emulator a Redfish interface resources as static or dynamically.

Static emulator is accomplish by copy a Redfish mockup in a ./static directory.

Dynamic emulator is accomplished by creating the Python files.  The code for an example resource (EgResource) is available to expedite the creation of dynamic resources.  The example is for a collection/member construct, EgResources/{id}.

The Swordfish model has been emulate using this emulator.  The repository is available at [Swordfish API Emulator](https://github.com/SNIA/Swordfish-API-Emulator).  The repository provides a good example of the Python files for dynamic resources.

The emulator is structure so it can be hosted on a standalone system or multiple instances in a Cloud Foundry.  Note: the cloud foundry method has be successful within a company internal cloud foundry service. It has not be attempted on a public cloud foundry service.

This program is a python35 program.  The program has been verified on 3.5.2.

## Installation

Before the emulator can be executed locally, specific Python packages need to be installed.

### Local Standalone

The required python packages for a local environment are listed in the file **./packageSets/Env-Local-Python3.5.2_requirements.txt**.  The file lists the Python package and revision.

The 'pip' command can be used to install the environment.

	pip install -r [packageSet]

The 'pip freeze' command can be used to display the installed packages and their revision.

### Cloud

The required python packages for a Cloud Foundry environment are listed in the file **./requirements.txt**.  The file lists the Python package, without the revision.
The packages will be installed automatically during invocation.

### Docker

Use one of these actions to pull or build the container:

* Pull the container from Docker Hub:

    ```bash
    docker pull dmtf/redfish-interface-emulator:latest
    ```
* Build a container from local source:

    ```bash
    docker build -t dmtf/redfish-interface-emulator:latest.
    ```
* Build a container from GitHub:

    ```bash
    docker build -t dmtf/redfish-interface-emulator:latest https://github.com/DMTF/Redfish-Interface-Emulator.git
    ```

## Invocation

### Standalone

Edit the emulator-config.json file and set **"MODE": "Local"**, then start the emulator.

	python emulator.py

### Cloud Foundry

Edit the emulator-config.json file and set **"MODE": "Cloud"**, then push the emulator to the foundry.

	cf push [foundry-app-name]

The **foundry-app-name** determines the URL for the Redfish service.

The cloud foundry makes use of the following files: requirements.txt, runtime.txt, and Profile. So they should exists in the same directory as emulator.py.

### Docker

This command runs the container with the built-in mockup:

```bash
docker run --rm dmtf/redfish-interface-emulator:latest
```

## Configuring the Emulator
The behavior of the emulator can be control via command line flags or property values in emulator-config.json.

### Emulator app flags

The emulator is invoked with the following command:

    python emulator.py [-h] [-v] [-port PORT] [-debug]
    -h -- help (gives syntax and usage) 
    -v -- verbose
    -port -- specifies the port number to use
    -debug -- enables debugging (needed to debug flask calls)

### Format of emulator-config.json

The emulator reads the emulator-config.json file to configure its behavior.
    
    {
        "MODE": "Local"
        "HTTPS": "Disable",
        "SPEC": "Redfish",
        "STATIC": "Enable",
        "TRAYS": [
            "./Resources/Systems/1/index.json"
        ]
        "POPULATE": "Emulator"
    }


* The MODE property specifies port to use. If the value is 'Cloud', the port is assigned by the cloud foundry. If the value is ‘Local’, the port is assigned the value of the port parameter is the command line or 5000, by default. (e.g. localhost:5000/redfish/v1)
* The HTTPS property specifies whether HTTP or HTTPS will used by the client
* The STATIC property specifies whether the emulator runs with the mockups in ./api_emulator/redfish/static
* The SPEC property specifies whether the computer system is represented as a Redfish ComputerSystem (SPEC = “Redfish”) or another schema.
* The TRAYS property specifies the path to the resources that will make up the initial resource pools. These simple resource pools are depleted as computer systems are composed. Multiple trays can be specified.
* The POPULATE property specifies the path to the file used by the INFRAGEN module to populate the Redfish Interface backend. If the file does not exist or if POPULATE is not defined, the emulator will start empty.

Three sample configuration files are provided:

* emulator-config_static.json (default) - start emulator with the static mockup
* emulator-dontpopulate.json - start emulator with no chassis or systems
* emulator-populate.json - start emulator and populate with **infragen**

### HTTPS
The emulator supports HTTP and HTTPS connections.  HTTPS is enabled by setting the HTTPS property in emulator-config.json.

    {
        "HTTPS": "Enable",
 		...
    }

When HTTPS is enabled, the emulator looks for the files: **server.crt** and **server.key** in the same directory as emulator.py.  The certificate file and key file can be self-signed or obtained from a certificate authority.

## Static emulation of a mockup

The emulator can be used to support mockups, statically. The means on HTTP GETs will work.  This can be done by just copying the mockup hierarchy to the ./static folder.

The static mockup is found in the directory ./api_emulator/redfish/static.  The emulator comes with a sample Redfish mockup.  This can be replaced with any mockup folder. The Redfish Forum has posted several of their mockups in [DSP2043](https://www.dmtf.org/sites/default/files/DSP2043_1.2.0.zip).

Note: If the new mockup has additional resources in the ServiceRoot, then modifications need to be made in static_resource_emulator.py to adds these new resources.

## Dynamic emulation
The emulator was designed to support dynamic resources.  This requires that Python code exists for each dynamic resource. Resources can be incremental recasted as dynamic, so one can straddle static vs dynamic emulation, with some resources static while others are dynamic.

The following outlines the overall process. More complete documentation is in a Word document in the ./doc directory.  An example for the Chassis resource is included in the source code.

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

To automate step #1 and #2, above, a code generator exists in the ./codegen directory.

#### Auto-generate the API file
To generate a API file, execute the following command

	codegen_api [mockup] [outputdir]

Where

* \[mockup\] is the name of the singleton resource
* \[outputdir\] is the directory for the API file
* The command uses the index.json file in the current work directory as input

The generated code supports the HTTP GET, PATCH, POST and DELETE commands

If the resource has subordinate resources that need to be instantiated when this resource is instantiated, that code will need to be manually added.

#### Auto-generate the template file
To generate a template file, execute the following command

	codegen_template [mockup] [outputdir]

Where

* \[mockup\] is the name of the singleton resource
* \[outputdir\] is the directory for the API file
* The command uses the index.json file in the current work directory as input   
   
 (TODO - add the filename as a command line parameter)

The codegen_template source file contains a dictionary with the names of Redfish collections and their corresponding wildcard.  This dictionary needs to be manually updated to the keep in sync with Redfish modeling. 

## Populating the dynamic emulator - INFRAGEN Module

Once a resource is made dynamic, the emulator can either start up with no members in its collections or some initial set of members.

To populate the Redfish model, set the POPULATE property in emulator-config.json.

    {
        "POPULATE": "Emulator",
		. . .
    }

Once the emulator has started, it will read the file **./infragen/populate-config.json**.  This file contains a JSON structure which specifies resources to populate.  The following example specifies that 5 Chassis be instantiated and linked to 5 Systems.

```
{
  "POPULATE": {
    "Chassis": [
      {
        "Name": "Compute Chassis",
        "Id": "Chassis-{0}",
        "Count": 5,
        "Links": {
          "ComputerSystems": [
            {
              "Name": "Compute System",
              "Id": "System-{0}",
              "Count": 1,
              "Processors": [
                {
                  "Id": "CPU{0}",
                  "TotalCores": 12,
                  "MaxSpeedMHz": 2400,
                  "Count": 2
                }
              ],
              "Memory": [
                {
                  "Id": "DRAM{0}",
                  "CapacityMiB": 16384,
                  "MemoryType": "DRAM",
                  "Count": 4
                },
                {
                  "Id": "NVRAM{0}",
                  "CapacityMiB": 65536,
                  "MemoryType": "NVDIMM_N",
                  "Count": 4
                }
              ],
              "SimpleStorage": [
                {
                  "Id": "SAS-CTRL{0}",
                  "Count": 1,
                  "Devices": {
                    "CapacityBytes": 549755813888,
                    "Count": 1
                  }
                }
              ],
              "EthernetInterfaces": [
                {
                  "Id": "NIC-{0}",
                  "SpeedMbps": 10000,
                  "Count": 2
                }
              ]
            }
          ]
        }
      },
```

### INFRAGEN module

The INFRAGEN module is used to populate the Redfish Interface with members (Chassis, Systems, Resource Blocks, Resources Zones, Processors, Memory, etc).

This module is execute by emulator.py once the emulator is up and reads the populate-config.json file.

The tool generate_template.py can be used to help a user with the creation of JSON template according to a specific Redfish schema by guiding the user through the schema and asking for input values. This module runs independently of the populate function and from the emulator itself.

## Testing the (dynamic) Emulator

The following is the general command for running unit test.

    python unittests.py <SPEC> "<PATH>"

Where

* <SPEC> should correspond to the value in emulator-config.json
* <PATH> is the path to use for testing and should be enclosed in double-quotes
* Example: python unittests.py Redfish "localhost:5000"

Once the command completes, inspect the log file which is produced, "test-rsa-emulator.log".

The command to test the emulator can executed against the emulator running locally or hosted in the cloud.

## Composition GUI

Generally, Postman is used to interact with the Redfish interface. However, a web GUI is available for testing the composition service, including the ability to compose and delete systems.

* Compose
	* Navigate to /CompositionService/ResourceZones/\<ZONE\>/, a check box appears next to each Resource Block
	* Select the Resource Blocks to use to compose a system
	* Press the button "compose" on the top of the webpage
* Delete
	* Navigate the browser to /Systems/\<SYSTEM\>/, if the system is of type "COMPOSED", a "delete" button appears
	* Select the delete button and the composed system will be deleted

Screenshots of the browser available in /doc/browser-screenshots.pdf

To use, point a brower to the URI **http://localhost:5000/browse.html**

## Release Process

Run the `release.sh` script to publish a new version.

```bash
sh release.sh <NewVersion>
```

Enter the release notes when prompted; an empty line signifies no more notes to add.
