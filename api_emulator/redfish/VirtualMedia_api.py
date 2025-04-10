import logging
import traceback
from flask import request
from flask_restful import Resource

from .templates.VirtualMediaCollection import get_virtual_media_collection_instance
from .templates.VirtualMedia import get_virtual_media_instance

INTERNAL_ERROR = 500

members = ["CD", "Floppy", "USBStick", "DVD"]  # List of member IDs
member_data = {}  # Dictionary to store detailed member data


class VirtualMediaCollectionAPI(Resource):
    def __init__(self, **kwargs):
        self.rb = kwargs.get('rb', '')
        logging.info('VirtualMediaCollectionAPI initialized')

    def get(self, ident):
        try:
            data = get_virtual_media_collection_instance(
                wildcards={"rb": self.rb, "manager_id": ident},
                member_ids=members
            )
            return data, 200
        except Exception:
            traceback.print_exc()
            return {"error": "Internal server error"}, INTERNAL_ERROR
        
class VirtualMediaAPI(Resource):
    def __init__(self, **kwargs):
        self.rb = kwargs.get('rb', '')
        logging.info('VirtualMediaAPI initialized')
    def get(self, ident1, ident2):
        try:
            global member_data
            if ident2 not in member_data.get(ident1, {}):
                if ident1 not in member_data:
                    member_data[ident1] = {}
                member_data[ident1][ident2] = get_virtual_media_instance(wildcards={"rb": self.rb, "manager_id": ident1, "member_id":ident2})
            return member_data[ident1][ident2], 200
        except Exception:
            traceback.print_exc()
            return {"error": "Internal server error"}, INTERNAL_ERROR


class VirtualMediaEjectAPI(Resource):
    def __init__(self, **kwargs):
        self.rb = kwargs.get('rb', '')
        logging.info('VirtualMediaEjectAPI initialized')
    
    def post(self, ident1, ident2):
        try:
            global member_data
            if ident2 not in member_data.get(ident1, {}):
                if ident1 not in member_data:
                    member_data[ident1] = {}
                member_data[ident1][ident2]= get_virtual_media_instance(wildcards={"rb": self.rb, "manager_id": ident1, "member_id":ident2})    
            member_data[ident1][ident2]["Inserted"]= False
            member_data[ident1][ident2]["Image"]= None
            member_data[ident1][ident2]["ImageName"]= None
            member_data[ident1][ident2]["ConnectedVia"]="NotConnected"
            return member_data[ident1][ident2], 200
        except Exception:
            traceback.print_exc()
            return INTERNAL_ERROR
        
class VirtualMediaInsertAPI(Resource):
    def __init__(self, **kwargs):
        self.rb = kwargs.get('rb', '')
        logging.info('VirtualMediaInsertAPI initialized')
    
    def post(self, ident1, ident2):
        try:
            global member_data
            if ident2 not in member_data.get(ident1, {}):
                if ident1 not in member_data:
                    member_data[ident1] = {}
                member_data[ident1][ident2]= get_virtual_media_instance(wildcards={"rb": self.rb, "manager_id": ident1, "member_id":ident2})    
            if not request.json:
                return "Invalid input, expected JSON", 400
            for key, value in request.json.items():
                member_data[ident1][ident2][key]= value
            
            member_data[ident1][ident2]["Inserted"]= True
            return member_data[ident1][ident2], 200
        except Exception:
            traceback.print_exc()
            return INTERNAL_ERROR