#-----------------------------------------------------------------------------
# INTEL CONFIDENTIAL
# Copyright 2015 Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related to
# the source code ("Material") are owned by Intel Corporation or its suppliers
# or licensors. Title to the Material remains with Intel Corporation or its
# suppliers and licensors. The Material contains trade secrets and proprietary
# and confidential information of Intel or its suppliers and licensors. The
# Material is protected by worldwide copyright and trade secret laws and
# treaty provisions. No part of the Material may be used, copied, reproduced,
# modified, published, uploaded, posted, transmitted, distributed, or
# disclosed in any way without Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be
# express and approved by Intel in writing.
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
# Author...: Manasa M Kalburgi
# E-mail...: kevin.midkiff@intel.com
# Date.....: 6/11/2015
# Version..: 0.1
#-----------------------------------------------------------------------------
import copy

_THERMAL_TEMPLATE = \
    {
        "@odata.context": "{rb}$metadata#Chassis/Links/Members/{ch_id}/Links/Thermal/$entity",
        "@odata.id": "{rb}Chassis/{ch_id}/Thermal",
        "@odata.type": "#Thermal.v1_0_0.Thermal",
        "Id": "Thermal",
        "Name": "Thermal Metrics",
        #"Modified": None,
        "Temperatures": [
            {
                
            "@odata.id": "{rb}Chassis/{ch_id}/Thermal#/Temperatures/0",
            "MemberId": "0",
            "Name": "CPU1 Temp",
            "SensorNumber": 42,
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "ReadingCelcius": 21,
            "UpperThresholdNonCritical": 42,
            "UpperThresholdCritical": 42,
            "UpperThresholdFatal": 42,
            "LowerThresholdNonCritical": 42,
            "LowerThresholdCritical": 5,
            "LowerThresholdFatal": 42,
            "MinimumValue": 0,
            "MaximumValue": 200,
            "PhysicalContext": "CPU",
            "RelatedItem": [
                {"@odata.id": "{rb}Systems/{ch_id}#/Processors/0" }
            ]
        
                #"CorrelatableID": "ReferenceToAPotentialThingLikeAProcessor"
            },
            {
            "@odata.id": "{rb}Chassis/{ch_id}/Thermal#/Temperatures/1",
            "MemberId": "1",
            "Name": "CPU2 Temp",
            "SensorNumber": 43,
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "ReadingCelsius": 21,
            "UpperThresholdNonCritical": 42,
            "UpperThresholdCritical": 42,
            "UpperThresholdFatal": 42,
            "LowerThresholdNonCritical": 42,
            "LowerThresholdCritical": 5,
            "LowerThresholdFatal": 42,
            "MinReadingRange": 0,
            "MaxReadingRange": 200,
            "PhysicalContext": "CPU",
            "RelatedItem": [
                {"@odata.id": "{rb}Systems/{ch_id}#/Processors/1" }
            ]
        },

            {
            "@odata.id": "{rb}Chassis/{ch_id}/Thermal#/Temperatures/2",
            "MemberId": "2",
            "Name": "Chassis Intake Temp",
            "SensorNumber": 44,
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "ReadingCelsius": 25,
            "UpperThresholdNonCritical": 30,
            "UpperThresholdCritical": 40,
            "UpperThresholdFatal": 50,
            "LowerThresholdNonCritical": 10,
            "LowerThresholdCritical": 5,
            "LowerThresholdFatal": 0,
            "MinReadingRange": 0,
            "MaxReadingRange": 200,
            "PhysicalContext": "Intake",
            "RelatedItem": [
                {"@odata.id": "{rb}Chassis/{ch_id}" },
                {"@odata.id": "{rb}Systems/{ch_id}" }
            ]
        }
    ],
    
           
        "Fans": [
            {
                "@odata.id":"{rb}Chassis/{ch_id}/Thermal#/Fans/0",
                "MemberId":"0",
                "FanName": "BaseBoard System Fan",
                "PhysicalContext": "Backplane",
                "Status": {
                    "State": "Enabled",
                    "Health": "OK"
                },
                "ReadingRPM": 2100,
                "UpperThresholdNonCritical": 42,
                "UpperThresholdCritical": 4200,
                "UpperThresholdFatal": 42,
                "LowerThresholdNonCritical": 42,
                "LowerThresholdCritical": 5,
                "LowerThresholdFatal": 42,
                "MinReadingRange": 0,
                "MaxReadingRange": 5000,
                "Redundancy" : [
                {"@odata.id": "{rb}Chassis/{ch_id}/Thermal#/Redundancy/0"}
            ],
            "RelatedItem" : [
                {"@odata.id": "{rb}Systems/{ch_id}" },
                {"@odata.id": "{rb}Chassis/{ch_id}" }
            ]

            },
            {
                "@odata.id": "{rb}Chassis/{ch_id}/Thermal#/Fans/1",
                "MemberId": "1",
                "FanName": "BaseBoard System Fan Backup",
                #"CorrelatableID": "Chassis/1/Fan2",
                "PhysicalContext": "Backplane",
                "Status": {
                    "State": "Enabled",
                    "Health": "OK"
                },
                #"Units": "RPM",
                "ReadingRPM": 2100,
                "UpperThresholdNonCritical": 42,
                "UpperThresholdCritical": 4200,
                "UpperThresholdFatal": 42,
                "LowerThresholdNonCritical": 42,
                "LowerThresholdCritical": 5,
                "LowerThresholdFatal": 42,
                "MinReadingRange": 0,
                "MaxReadingRange": 5000,
                "Redundancy" : [
                {"@odata.id": "{rb}Chassis/{ch_id}/Power#/Redundancy/0"}
            ],
            "RelatedItem" : [
                {"@odata.id": "{rb}Systems/{ch_id}" },
                {"@odata.id": "{rb}Chassis/{ch_id}" }
            ] 

                
            }
        ],
        "Redundancy": [
            {
                "@odata.id": "{rb}Chassis/{ch_id}/Thermal#/Redundancy/0",
                "MemberId": "0",
                "Name": "BaseBoard System Fans",
                "RedundancySet": [
                { "@odata.id": "{rb}Chassis/{ch_id}/Thermal#/Fans/0" },
                { "@odata.id": "{rb}Chassis/{ch_id}/Thermal#/Fans/1" }
            ],

                "Mode": "N+1",
                "Status": {
                    "State": "Enabled",
                    "Health": "OK"
                },
                "MinNumNeeded": 1,
                "MaxNumSupported": 2
            }
        ]
    }


def get_thermal_template(rest_base, ch_id):
    """
    Returns a formatted template

    Arguments:
        rest_base - Base URL of the RESTful interface
        ident     - Identifier of the chassis
    """
    c = copy.deepcopy(_THERMAL_TEMPLATE)

    c['@odata.context'] = c['@odata.context'].format(rb=rest_base, ch_id=ch_id)
    c['@odata.id'] = c['@odata.id'].format(rb=rest_base, ch_id=ch_id)
    c['Redundancy'][0]['@odata.id']=c['Redundancy'][0]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Fans'][0]['@odata.id']=c['Fans'][0]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Fans'][1]['@odata.id']=c['Fans'][1]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Temperatures'][0]['@odata.id']=c['Temperatures'][0]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Temperatures'][0]['RelatedItem'][0]['@odata.id']=c['Temperatures'][0]['RelatedItem'][0]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    
    c['Temperatures'][1]['@odata.id']=c['Temperatures'][1]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Temperatures'][1]['RelatedItem'][0]['@odata.id']=c['Temperatures'][1]['RelatedItem'][0]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
   
    c['Temperatures'][2]['@odata.id']=c['Temperatures'][2]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Temperatures'][2]['RelatedItem'][0]['@odata.id']=c['Temperatures'][2]['RelatedItem'][0]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Temperatures'][2]['RelatedItem'][1]['@odata.id']=c['Temperatures'][2]['RelatedItem'][1]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Fans'][0]['Redundancy'][0]['@odata.id']=c['Fans'][0]['Redundancy'][0]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Fans'][0]['RelatedItem'][0]['@odata.id']=c['Fans'][0]['RelatedItem'][0]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Fans'][0]['RelatedItem'][1]['@odata.id']=c['Fans'][0]['RelatedItem'][1]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Fans'][1]['Redundancy'][0]['@odata.id']=c['Fans'][1]['Redundancy'][0]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Fans'][1]['RelatedItem'][0]['@odata.id']=c['Fans'][1]['RelatedItem'][0]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Fans'][1]['RelatedItem'][1]['@odata.id']=c['Fans'][1]['RelatedItem'][1]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Redundancy'][0]['RedundancySet'][0]['@odata.id']=c['Redundancy'][0]['RedundancySet'][0]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    c['Redundancy'][0]['RedundancySet'][1]['@odata.id']=c['Redundancy'][0]['RedundancySet'][1]['@odata.id'].format(rb=rest_base,ch_id=ch_id)
    
    return c
