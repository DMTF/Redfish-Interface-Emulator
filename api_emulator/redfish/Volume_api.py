import logging
import traceback
from flask import request
from flask_restful import Resource

import uuid
from .Drive_api import Drive_API, drive_config
from .templates.Volumes import get_volume_instance
from .templates.VolumeCollection import get_volume_collection_instance

INTERNAL_ERROR = 500

volume_members = {}
volume_data = {}
class VolumeCollectionAPI(Resource):
    def __init__(self, **kwargs):
        self.rb = kwargs.get('rb', '')
        logging.info('VolumeCollectionAPI initialized')

    def get(self, ident1, ident2):
        try:

            data = get_volume_collection_instance(
                wildcards={"rb": self.rb, "system_id":ident1, "storage_id": "Storage-1"}, 
                volume_ids=[]
            )
            if ident1 not in volume_members:
                volume_members[ident1] = {}
                if ident2 not in volume_members[ident1]:
                    volume_members[ident1][ident2] = {}
            if len(volume_members[ident1][ident2])>0:
                vids = []
                for vid in volume_members[ident1][ident2]:
                    vids.append(vid)
                data = get_volume_collection_instance(
                wildcards={"rb": self.rb, "system_id":ident1, "storage_id": "Storage-1"}, 
                volume_ids=vids
                )
            return data, 200
        except Exception:
            traceback.print_exc()
            return {"error": "Internal server error"}, INTERNAL_ERROR
    
    def post(self, ident1, ident2):
        logging.info('VolumeCollectionAPI POST called')
        try:
            global config
            config = {}

            if ident1 not in volume_members:
                volume_members[ident1] = {}
            if ident2 not in volume_members[ident1]:
                volume_members[ident1][ident2] = {}

            # Assign the lowest available volume ID
            existing_ids = {
                int(vol_id.split('-')[-1])
                for vol_id in volume_members[ident1][ident2]
                if vol_id.startswith("Volume-")
            }
            volume_id = 1
            while volume_id in existing_ids:
                volume_id += 1

            req = request.json
            links = req['Links']['Drives']
            volume_uuid = str(uuid.uuid4())
            min_capacity_bytes = float('inf')
            drive_links = []

            # Check for duplicate drives in the request
            seen_paths = set()
            for link in links:
                dp = link["@odata.id"]
                if dp in seen_paths:
                    return {"error": f"Duplicate drive in request: {dp}"}, 400
                seen_paths.add(dp)

            system_number = ident1.split('-')[-1]

            # Validate all drives are from same chassis and valid range
            first_drive_path = links[0]["@odata.id"]
            first_chassis = first_drive_path.split('/')[-3]
            first_chassis_number = first_chassis.split('-')[-1]

            try:
                chassis_num_int = int(first_chassis_number)
            except:
                return {"error": f"Invalid chassis format in {first_chassis}"}, 400

            if chassis_num_int < 1 or chassis_num_int > 6:
                return {"error": f"Drive not found: {first_chassis}. Only chassis 1 to 6 are valid."}, 400

            if any(link["@odata.id"].split('/')[-3] != first_chassis for link in links):
                return {"error": "Cannot mix drives from different chassis in a single volume on a rackmount server."}, 400

            if system_number != first_chassis_number:
                return {"error": f"Only drives from Chassis-{system_number} can be used with {ident1}."}, 400

            used_drives = []  #Track all used drives

            for link in links:
                drive_path = link["@odata.id"]
                chassis_id = drive_path.split('/')[-3]
                drive_id = drive_path.split('/')[-1]
                full_drive_key = f"{chassis_id}/{drive_id}"

                try:
                    drive_num = int(drive_id.split('-')[-1])
                except:
                    return {"error": f"Invalid drive format in {drive_id}"}, 400

                if drive_num < 1 or drive_num > 6:
                    return {"error": f"Invalid drive: {drive_id}. Only Drive-1 to Drive-6 are allowed."}, 400

                drive_api = Drive_API(rb="/redfish/v1")
                response, status = drive_api.get(chassis_id, drive_id)

                if full_drive_key in drive_config and drive_config[full_drive_key]["Links"]["Volumes"]:
                    used_drives.append(drive_path)

                drive_links.append(drive_path)

                capacity = drive_config[chassis_id][drive_id]['CapacityBytes']
                if capacity < min_capacity_bytes:
                    min_capacity_bytes = capacity

            # After loop: check if any were used
            if used_drives:
                return {
                    "error": "The following drives are already in use by other volumes.",
                    "drives": used_drives
                }, 400

            n = len(drive_links)
            capacity_requested = req['CapacityBytes']
            raid_type = req['RAIDType']

            if raid_type == "RAID0":
                if n < 2:
                    return {"error": "RAID0 requires at least 2 drives."}, 400
                if capacity_requested > n * min_capacity_bytes:
                    return {"error": f"RAID0 max capacity exceeded: {n * min_capacity_bytes}"}, 400
            elif raid_type == "RAID1":
                if n < 2:
                    return {"error": "RAID1 requires at least 2 drives."}, 400
                if capacity_requested > min_capacity_bytes:
                    return {"error": f"RAID1 max capacity exceeded: {min_capacity_bytes}"}, 400
            elif raid_type == "RAID5":
                if n < 3:
                    return {"error": "RAID5 requires at least 3 drives."}, 400
                if capacity_requested > (n - 1) * min_capacity_bytes:
                    return {"error": f"RAID5 max capacity exceeded: {(n - 1) * min_capacity_bytes}"}, 400
            elif raid_type == "RAID6":
                if n < 4:
                    return {"error": "RAID6 requires at least 4 drives."}, 400
                if capacity_requested > (n - 2) * min_capacity_bytes:
                    return {"error": f"RAID6 max capacity exceeded: {(n - 2) * min_capacity_bytes}"}, 400
            elif raid_type == "RAID10":
                if n < 4 or n % 2 != 0:
                    return {"error": "RAID10 requires an even number of at least 4 drives."}, 400
                if capacity_requested > (n // 2) * min_capacity_bytes:
                    return {"error": f"RAID10 max capacity exceeded: {(n // 2) * min_capacity_bytes}"}, 400

            # Update drive links to point to this volume
            for drive_path in drive_links:
                chassis_id = drive_path.split('/')[-3]
                drive_id = drive_path.split('/')[-1]
                full_drive_key = f"{chassis_id}/{drive_id}"

                if full_drive_key not in drive_config:
                    drive_config[full_drive_key] = {"Links": {"Volumes": []}}

                drive_config[full_drive_key]["Links"]["Volumes"].append({
                    "@odata.id": f"{self.rb}Systems/{ident1}/Storage/{ident2}/Volumes/Volume-{volume_id}"
                })

            vid = f"Volume-{volume_id}"
            config = get_volume_instance(
                wildcards={"rb": self.rb, "system_id": ident1, "storage_id": ident2, "volume_id": volume_id, "durable_name": volume_uuid},
                drive_ids=drive_links,
                raid_type=raid_type,
                capacity_bytes=capacity_requested
            )
            volume_members[ident1][ident2][vid] = config
            return config, 201

        except Exception:
            traceback.print_exc()
            return {"error": "Internal server error"}, INTERNAL_ERROR

class VolumeAPI(Resource):
    def __init__(self, **kwargs):
        self.rb = kwargs.get('rb', '')
        logging.info('VolumeAPI initialized')
    def get(self, ident1, ident2, ident3):
        try:
            global config
            global wildcards
            durable_name = volume_members[ident1][ident2][ident3]['Identifiers'][0]['DurableName']
            drive_ids = []
            for id in volume_members[ident1][ident2][ident3]['Links']['Drives']:
                drive_ids.append(id['@odata.id'])
            capacity_bytes = volume_members[ident1][ident2][ident3]['CapacityBytes']
            raid_type = volume_members[ident1][ident2][ident3]['RAIDType']
            config = get_volume_instance({'rb':self.rb, 'system_id':ident1, 'storage_id':ident2, 'volume_id':ident3, 'durable_name':durable_name}, drive_ids=drive_ids, raid_type=raid_type, capacity_bytes=capacity_bytes)
            return config, 200
        except Exception:
            traceback.print_exc()
            return {"error": "Internal server error"}, INTERNAL_ERROR
    
    def delete(self, ident1, ident2, ident3):
        try:
            if ident1 not in volume_members:
                return {"error": f"System {ident1} not found."}, 404
            if ident2 not in volume_members[ident1]:
                return {"error": f"Storage {ident2} not found under system {ident1}."}, 404
            if ident3 not in volume_members[ident1][ident2]:
                return {"error": f"Volume {ident3} not found under system {ident1}, storage {ident2}."}, 404

            volume_data = volume_members[ident1][ident2][ident3]
            drive_links = volume_data["Links"]["Drives"]

            for link in drive_links:
                drive_path = link["@odata.id"]
                chassis_id = drive_path.split("/")[-3]
                drive_id = drive_path.split("/")[-1]
                full_drive_key = f"{chassis_id}/{drive_id}"

                if full_drive_key in drive_config:
                    if "Links" in drive_config[full_drive_key] and "Volumes" in drive_config[full_drive_key]["Links"]:
                        drive_config[full_drive_key]["Links"]["Volumes"] = []

            del volume_members[ident1][ident2][ident3]

            return {"message": f"Volume {ident3} deleted successfully."}, 204

        except Exception:
            traceback.print_exc()
            return {"error": "Internal server error"}, INTERNAL_ERROR
