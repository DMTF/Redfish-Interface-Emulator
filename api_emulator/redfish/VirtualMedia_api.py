import logging
import traceback
from flask import request
from flask_restful import Resource

from .templates.VirtualMedia import get_virtual_media_instance

INTERNAL_ERROR = 500

members = []  # List of member IDs
member_data = {}  # Dictionary to store detailed member data


class VirtualMediaAPI(Resource):
    def __init__(self, **kwargs):
        self.rb = kwargs.get('rb', '')
        logging.info('VirtualMediaAPI initialized')

    def get(self, ident):
        try:
            data = get_virtual_media_instance(
                wildcards={"rb": self.rb, "manager_id": ident},
                member_ids=members
            )
            return data, 200
        except Exception:
            traceback.print_exc()
            return {"error": "Internal server error"}, INTERNAL_ERROR

    def post(self, ident):
        try:
            req = request.get_json(force=True)
            new_member_id = req.get('MemberId')

            if not new_member_id:
                return {"error": "MemberId is required"}, 400

            if new_member_id in members:
                return {"error": "Member already exists"}, 409

            members.append(new_member_id)
            member_data[new_member_id] = req  # Save full data

            location = f"{self.rb}Managers/{ident}/VM1/{new_member_id}"
            return {"message": "Member created", "@odata.id": location}, 201
        except Exception:
            traceback.print_exc()
            return {"error": "Internal server error"}, INTERNAL_ERROR