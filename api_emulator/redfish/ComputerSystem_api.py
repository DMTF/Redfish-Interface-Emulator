# Copyright Notice:
# Copyright 2017 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/LICENSE.md

# Example Collection Resource and Singleton Resource
"""
Collection API  GET, POST
Singleton  API  GET, POST, PATCH, DELETE

"""
import g

import sys, traceback
import logging
import copy
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

from .templates.ComputerSystem import get_ComputerSystem_instance
from .ComputerSystem.ResetActionInfo_api import ResetActionInfo_API
from .ComputerSystem.ResetAction_api import ResetAction_API
from .processor import members as processors
from .memory import members as memory
from .ethernetinterface import members as ethernetinterfaces
from .simplestorage import members as simplestorage
from .ResourceBlock_api import members as resource_blocks

members = {}
foo = 'false'
INTERNAL_ERROR = 500

#ComputerSystem API
class ComputerSystemAPI(Resource):
    # kwargs is used to pass in the wildcards values to replace when the instance is created - via get_<resource>_instance().
    #
    # __init__ should store the wildcards and pass the wildcards to the get_<resource>_instance(). 
    def __init__(self, **kwargs):
        logging.basicConfig(level=logging.INFO)
        logging.info('ComputerSystemAPI init called')
        try:
            global config
            global wildcards
            wildcards = kwargs
        except Exception:
            traceback.print_exc()

    def memory_summary(self,ident):

        totalsysmem=sum([x['CapacityMiB']for x in memory.get(ident,{}).values() if x['MemoryType']=='DRAM'])
        totalpsysmem=sum([x['CapacityMiB']for x in memory.get(ident,{}).values() if 'NVDIMM' in x['MemoryType']])
        return {u'Status': {u'Health': 'OK', u'State': 'Enabled'},
                    u'TotalSystemMemoryGiB': totalsysmem,
                    u'TotalSystemPersistentMemoryGiB': totalpsysmem}


    def processor_summary(self,ident):

        procs=processors.get(ident,{}).values()
        if not procs:
            return {}
        return {u'Status': {u'Health': 'OK', u'State': 'Enabled'},
                    u'Count': len(procs),
                    u'Model': procs[0].get('Model','unknown')}


    # HTTP GET
    def get(self,ident):
        try:
            # Find the entry with the correct value for Id
            resp = 404
            if ident in members:
                conf= members[ident]
                conf['ProcessorSummary']=self.processor_summary(ident)
                conf['MemorySummary']=self.memory_summary(ident)
                resp = conf, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP POST
    # - Create the resource (since URI variables are avaiable)
    # - Update the members and members.id lists
    # - Attach the APIs of subordinate resources (do this only once)
    # - Finally, create an instance of the subordiante resources
    def post(self,ident):
        logging.info('ComputerSystemAPI PUT called')
        try:
            global config
            global wildcards
            wildcards['id'] = ident
            config=get_ComputerSystem_instance(wildcards)
            members[ident]=config
            global foo
            # Attach URIs for subordiante resources
            '''
            if  (foo == 'false'):
                # Add APIs for subordinate resourcs
                collectionpath = g.rest_base + "ComputerSystems/" + ident + "/EgSubResources"
                logging.info('collectionpath = ' + collectionpath)
                g.api.add_resource(EgSubResourceCollectionAPI, collectionpath, resource_class_kwargs={'path': collectionpath} )
                singletonpath = collectionpath + "/<string:ident>"
                logging.info('singletonpath = ' + singletonpath)
                g.api.add_resource(EgSubResourceAPI, singletonpath,  resource_class_kwargs={'rb': g.rest_base, 'eg_id': ident} )
                foo = 'true'
            '''
            # Create an instance of subordinate resources
            #cfg = CreateSubordinateRes()
            #out = cfg.put(ident)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('ComputerSystemAPI put exit')
        return resp

    # HTTP PATCH
    def patch(self, ident):
        logging.info('ComputerSystemAPI patch called')
        raw_dict = request.get_json(force=True)
        logging.info(raw_dict)
        try:
            # Find the entry with the correct value for Id
            config = members[ident]
            logging.info(config)
            for key, value in raw_dict.items():
                logging.info('Update ' + key + ' to ' + value)
                config[key] = value
            logging.info(config)
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


    # HTTP DELETE
    def delete(self,ident):
        # logging.info('ComputerSystemAPI delete called')
        try:
            #del(members[ident])
            resp = DeleteComposedSystem(ident)
            resp = 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


# ComputerSystem Collection API
class ComputerSystemCollectionAPI(Resource):
    def __init__(self):
        self.rb = g.rest_base
        self.config = {
            '@odata.context': self.rb + '$metadata#ComputerSystemCollection.ComputerSystemCollection',
            '@odata.id': self.rb + 'ComputerSystemCollection',
            '@odata.type': '#ComputerSystemCollection.1.0.0.ComputerSystemCollection',
            'Name': 'ComputerSystem Collection',
            'Links': {}
        }
        self.config['Links']['Member@odata.count'] = len(members)
        self.config['Links']['Members'] = [{'@odata.id':x['@odata.id']} for x in members.values()]

    def get(self):
        try:
            resp = self.config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # The POST command should be for adding multiple instances. For now, just add one.
    # Todo - Fix so the config can be passed in the data.
#    def post(self):
#        try:
#            logging.debug(request.get_json())
#            raise Exception('Not implemented')
#            resp=self.config,200
#        except Exception:
#            traceback.print_exc()
#            resp = INTERNAL_ERROR
#        return resp

    def post(self):
        resp = INTERNAL_ERROR
        req = request.get_json()

        if req is not None:
            composed_system = CreateComposedSystem(req)
            resp = composed_system, 200
        else:
            resp = INTERNAL_ERROR

        return resp


#class ComposedSystem(Resource):
#    def __init__(self):
#        pass

def CreateComposedSystem(req):
        rb = g.rest_base
        status = False      # if the request can be processed, status will become True

        # Verify Existence of Resource Blocks
        blocks = req['Links']['ResourceBlocks']
        map_zones = dict()

        resource_ids={'Processors':[],'Memory':[],'SimpleStorage':[],'EthernetInterfaces':[]}

        for block in blocks:
            block = block['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
            if block in resource_blocks:
                zones = resource_blocks[block]['Links']['Zones']
                for zone in zones:
                    if block in map_zones.keys():
                        map_zones[block].append(zone['@odata.id'].replace(rb + 'CompositionService/ResourceZones/',''))
                    else:
                        map_zones[block] = [zone['@odata.id'].replace(rb + 'CompositionService/ResourceZones/','')]

                for device_type in resource_ids.keys():
                    for device in resource_blocks[block][device_type]:
                        resource_ids[device_type].append(device)

            else:
                # One of the Resource Blocks in the request does not exist
                resp = INTERNAL_ERROR

        # Verify that they all are under, at least, one Resource Zone
        for k1 in map_zones.keys():
            counter = 0
            for k2 in map_zones.keys():
                if k1==k2:
                    break
                for item in map_zones[k1]:
                    if item in map_zones[k2]:
                        counter = counter +1
                        if counter == len(map_zones.keys()):
                            break
                if counter == len(map_zones.keys()):
                            break
            if counter == len(map_zones.keys()):
                            status = True
                            break


        if status == True:
            if req['Name'] not in members.keys():

                # Create Composed System
                new_system = CreateComputerSystem(resource_class_kwargs={'rb': g.rest_base, 'linkChassis': [], 'linkMgr': None})
                new_system.put(req['Name'])

                # Remove unecessary Links and add ResourceBlocks to Links (this is a bit of a hack though)
                del members[req['Name']]['Links']['ManagedBy']
                del members[req['Name']]['Links']['Chassis']
                del members[req['Name']]['Links']['Oem']

                # This should be done through the CreateComputerSystem
                members[req['Name']]['SystemType'] = 'Composed'

                members[req['Name']]['Links']['ResourceBlocks']=[]


                # Add links to Processors, Memory, SimpleStorage, etc
                for device_type in resource_ids.keys():
                    for device in resource_ids[device_type]:
                        if device_type == 'Processors':
                            device = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            device_back = device
                            block = device.split('/', 1)[0]
                            device = device.split('/', 1)[-1]
                            device = device.split('/', 1)[-1]
                            try:
                                processors[req['Name']][device_back] = processors[block][device]
                            except:
                                processors[req['Name']] = {}
                                processors[req['Name']][device_back] = processors[block][device]
                        elif device_type == 'Memory':
                            device = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            device_back = device
                            block = device.split('/', 1)[0]
                            device = device.split('/', 1)[-1]
                            device = device.split('/', 1)[-1]
                            try:
                                memory[req['Name']][device_back] = memory[block][device]
                            except:
                                memory[req['Name']] = {}
                                memory[req['Name']][device_back] = memory[block][device]
                        elif device_type == 'SimpleStorage':
                            device = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            device_back = device
                            block = device.split('/', 1)[0]
                            device = device.split('/', 1)[-1]
                            device = device.split('/', 1)[-1]
                            try:
                                simplestorage[req['Name']][device_back] = simplestorage[block][device]
                            except:
                                simplestorage[req['Name']] = {}
                                simplestorage[req['Name']][device_back] = simplestorage[block][device]
                        elif device_type == 'EthernetInterfaces':
                            device = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            device_back = device
                            block = device.split('/', 1)[0]
                            device = device.split('/', 1)[-1]
                            device = device.split('/', 1)[-1]
                            try:
                                ethernetinterfaces[req['Name']][device_back] = ethernetinterfaces[block][device]
                            except:
                                ethernetinterfaces[req['Name']] = {}
                                ethernetinterfaces[req['Name']][device_back] = ethernetinterfaces[block][device]


                # Add ResourceBlocks to Links
                for block in blocks:
                    members[req['Name']]['Links']['ResourceBlocks'].append({'@odata.id': block['@odata.id']})


                # Update Resource Blocks affected
                for block in blocks:
                    block = block['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                    resource_blocks[block]['CompositionStatus']['CompositionState'] = 'Composed'
                    resource_blocks[block]['Links']['ComputerSystems'].append({'@odata.id': members[req['Name']]['@odata.id']})

                return members[req['Name']]
            else:
                # System Name already exists
                return INTERNAL_ERROR

        else:
            return INTERNAL_ERROR

        return req


def DeleteComposedSystem(ident):
    rb = g.rest_base
    resource_ids={'Processors':[],'Memory':[],'SimpleStorage':[],'EthernetInterfaces':[]}

    # Verify if the System exists and if is of type - "SystemType": "Composed"
    if ident in members:
        if members[ident]['SystemType'] == 'Composed':

            # Remove Links to Composed System and change CompositionState (to 'Unused') in associated Resource Blocks

            for block in members[ident]['Links']['ResourceBlocks']:
                block = block['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                resource_blocks[block]['Links']['ComputerSystems']
                for index, item in enumerate(resource_blocks[block]['Links']['ComputerSystems']):
                    if resource_blocks[block]['Links']['ComputerSystems'][index]['@odata.id'].replace(rb + 'Systems/','') == ident:
                        del resource_blocks[block]['Links']['ComputerSystems'][index]
                        resource_blocks[block]['CompositionStatus']['CompositionState'] = 'Unused'

                        for device_type in resource_ids.keys():
                            for device in resource_blocks[block][device_type]:
                                resource_ids[device_type].append(device)

            # Remove links to Processors, Memory, SimpleStorage, etc
            for device_type in resource_ids.keys():
                    for device in resource_ids[device_type]:
                        if device_type == 'Processors':
                            device_back = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            del processors[ident][device_back]
                            if processors[ident]=={}: del processors[ident]
                        elif device_type == 'Memory':
                            device_back = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            del memory[ident][device_back]
                            if memory[ident]=={}: del memory[ident]
                        elif device_type == 'SimpleStorage':
                            device_back = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            del simplestorage[ident][device_back]
                            if simplestorage[ident]=={}: del simplestorage[ident]
                        elif device_type == 'EthernetInterfaces':
                            device_back = device['@odata.id'].replace(rb + 'CompositionService/ResourceBlocks/','')
                            del ethernetinterfaces[ident][device_back]
                            if ethernetinterfaces[ident]=={}: del ethernetinterfaces[ident]

            # Remove Composed System from System list
            del members[ident]
            resp = 200
        else:
            # It is not a Composed System and therefore cannot be deleted as such"
            return INTERNAL_ERROR
    #

    return resp

def UpdateComposedSystem(req):
    resp = 201

    return resp

# CreateComputerSystem
#
# Called internally to create a instances of a resource.  If the resource has subordinate resources,
# those subordinate resource(s)  should be created automatically.
#
# This routine can also be used to pre-populate emulator with resource instances.  For example, a couple of
# Chassis and a ComputerSystem (see examples in resource_manager.py)
#
# Note: this may not the optimal way to pre-populate the emulator, since the resource_manager.py files needs
# to be editted.  A better method is just hack up a copy of usertest.py which performs a POST for each resource
# instance desired (e.g. populate.py).  Then one could have a multiple 'populate' files and the emulator doesn't
# need to change.
# 
# Note: In 'init', the first time through, kwargs may not have any values, so we need to check.
#   The call to 'init' stores the path wildcards. The wildcards are used when subsequent calls instanctiate
#   resources to modify the resource template.
#
class CreateComputerSystem(Resource):
    def __init__(self, **kwargs):
        logging.info('CreateComputerSystem init called')
        logging.debug(kwargs)#, kwargs.keys(), 'resource_class_kwargs' in kwargs)
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])
            logging.debug(wildcards)#, wildcards.keys())

    # Attach APIs for subordinate resource(s). Attach the APIs for a resource collection and its singletons
    def put(self,ident):
        logging.info('CreateComputerSystem put called')
        try:
            global config
            global wildcards
            wildcards['id'] = ident
            wildcards['sys_id'] = ident
            config=get_ComputerSystem_instance(wildcards)
            members[ident]=config

            ResetAction_API(resource_class_kwargs={'rb': g.rest_base,'sys_id': ident})
            ResetActionInfo_API(resource_class_kwargs={'rb': g.rest_base,'sys_id': ident})

            '''
            # attach subordinate resources
            collectionpath = g.rest_base + "ComputerSystems/" + ident + "/EgSubResources"
            logging.info('collectionpath = ' + collectionpath)
            g.api.add_resource(EgSubResourceCollectionAPI, collectionpath, resource_class_kwargs={'path': collectionpath} )
            singletonpath = collectionpath + "/<string:ident>"
            logging.debug('singletonpath = ' + singletonpath)
            g.api.add_resource(EgSubResourceAPI, singletonpath,  resource_class_kwargs={'rb': g.rest_base, 'eg_id': ident} )
            '''
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateComputerSystem init exit')
        return resp
