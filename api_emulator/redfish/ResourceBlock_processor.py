# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Redfish Processors and Processor Resources. Based on version 1.0.0

from flask_restful import Resource
from .templates.processor import format_processor_template
import logging

members = {}
INTERNAL_ERROR = 500


class ResourceBlock_Processor(Resource):
    """
    Processor.1.0.0.Processor
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        resp = 404
        if ident1 not in members:
            return 'not found',404
        if ident2 not in members[ident1]:
            return 'not found',404
        return members[ident1][ident2], 200


def Create_ResourceBlock_Processor(**kwargs):

    suffix_id = kwargs['suffix_id']
    resource_id = kwargs['processor_id']
    if suffix_id not in members:
        members[suffix_id] = {}
    members[suffix_id][resource_id] = format_processor_template(**kwargs)

