import json

from flask import jsonify
from flask.ext.restful import Resource
import psutil

from constants import PATHS


class SystemDetaislAPI(Resource):
    def get(self):
        details = psutil.virtual_memory()
        data = {
            'total_disk_space': details.total,
            'available_space': details.available,
            'used_space': details.used,
            'percentage_used': details.percent
        }

        return jsonify(data)


class SystemMemoryDetaislAPI(Resource):

    def __init__(self):
        self.root = PATHS['Root']

    def get(self):
        path = '{}StorageServices/FileService/StoragePools/BasePool/index.json'.format(PATHS['Root'])
        try:
            details = open(path)
            data = json.load(details)
            data = data['CapacitySources'][0]['ProvidedCapacity']
            c = {}
            for k, v in data.items():
                if k == "AllocatedBytes" and data['AllocatedBytes']:
                    c['total'] = data['AllocatedBytes']
                if k == "ConsumedBytes" and data['ConsumedBytes']:
                    c['consumed'] = data['ConsumedBytes']

            c['remaining'] = c['total'] - c['consumed']

        except Exception as e:
            return {"error": "Unable read file because of following error::{}".format(e)}, 500

        return jsonify(c)
