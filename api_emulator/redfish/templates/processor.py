# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# format_processor_template()

PROCESSOR_TEMPLATE = {
    "@odata.context": "{rb}$metadata#{suffix}/Links/Members/{cs_puid}/Processors/Links/Members/$entity",
    "@odata.id": "{rb}{suffix}/{cs_puid}/Processors/{id}",
    "@odata.type": "#Processor.1.0.0.Processor",
    "Name":"Processor",
    "Id": None,
    "Socket": "CPU {socket}",
    "ProcessorType": "CPU",
    "ProcessorArchitecture": "x86",
    "InstructionSet": "x86-64",
    "Manufacturer": "Intel(R) Corporation",
    "Model": "Multi-Core Intel(R) Xeon(R) processor 7xxx Series",
    "ProcessorId":{
        "VendorId":"GenuineIntel",
        "IdentificationRegisters":"0x34AC34DC8901274A",
        "EffectiveFamily": "0x42",
        "EffectiveModel": "0x61",
        "Step": "0x1",
        "MicrocodeInfo": "0x429943"
  },
    "MaxSpeedMHz": None,
    "TotalCores": None,
    "TotalThreads": None,
    "Status": None
}


def format_processor_template(rb, suffix, cs_puid, ident, socket, max_mhx,
                              total_cores, enabled_cores, total_threads,
                              enabled_threads, status):
    """
    Format the processor template -- returns the template
    """
    c = PROCESSOR_TEMPLATE.copy()
    c['@odata.context'] = c['@odata.context'].format(rb=rb, suffix=suffix, cs_puid=cs_puid)
    c['@odata.id'] = c['@odata.id'].format(rb=rb, suffix=suffix, cs_puid=cs_puid, id=ident)
    c['Id'] = str(ident)
    c['Socket'] = c['Socket'].format(socket=socket)
    c['MaxSpeedMHz'] = max_mhx
    c['TotalCores'] = total_cores
    c['TotalThreads'] = total_threads
    c['Status'] = status
    return c
