from mongoengine import connect
from mongoengine.errors import ValidationError

from db_uploader.config import MONGODB_URI
from db_uploader.schema import UploadVehicleInfo, ImageInfo

connect(host=MONGODB_URI)
from typing import Dict, List

from db_uploader import cloudinary_upload
from db_uploader.model.camera_info import CameraInfos
from db_uploader.model.images import Images
from db_uploader.model.record_videos import RecordVideos
from db_uploader.model.vehicle import Vehicles

def save_image(image_b64: str, link_folder: str):
    """Upload image in JPEG base 64 format to Cloudinary, then upload Image data to Mongo Db
    Return:
        (str): Document's UUID
    """
    try:
        response_image = cloudinary_upload.upload_image(image_b64, link_folder)
        image_data = ImageInfo(
            asset_id = response_image["asset_id"],
            public_id = response_image["public_id"],
            url = response_image["url"],
            secure_url = response_image["secure_url"],
            format = response_image["format"],
            created_at=response_image["created_at"]
        )
        
        return image_data.convertDictImageInfo()
    except Exception as exp: 
        return None

def save_video_get_id(video_record: RecordVideos):
    try:        
        video_data:RecordVideos = video_record.save()
        return video_data.id
    except ValidationError:
        raise Exception("Recorded video data format is incorrect")

def save_vehicle_info(vehicle_info: UploadVehicleInfo, video_id: str):
    try:
        vehicle_images: List[ImageInfo] = []
        lp_images: List[ImageInfo] = []

        for vehicle_image_data in vehicle_info.vehicle_images:
            vehicle_images.append(save_image(vehicle_image_data.jpeg_base64, vehicle_image_data.folder))

        for lp_image_data in vehicle_info.lp_images:
            lp_images.append(save_image(lp_image_data.jpeg_base64, lp_image_data.folder))

        preview_image  = save_image(vehicle_info.preview_image.jpeg_base64, vehicle_info.preview_image.folder)
        
        data = Vehicles(
            camera_id = vehicle_info.camera_id,
            vehicle_images = vehicle_images,
            plate_images = lp_images,
            video_id = video_id,
            record_time = vehicle_info.record_time,
            start_frame = vehicle_info.start_frame,
            end_frame = vehicle_info.end_frame,
            lp_labels = vehicle_info.lp_labels,
            preview_image = preview_image,
            vehicle_type = vehicle_info.type
        )
        data.save()
        return True
    except ValidationError as e:
        print(e)
        print("Data format is incorrect")
        return False

def upload_detected_vehicles(vehicle_data: List[UploadVehicleInfo], record_video: RecordVideos):
    try:
        video_id = save_video_get_id(record_video)

        for idx, data in enumerate(vehicle_data):
            flag = save_vehicle_info(data, video_id)
            if not flag:
                print(f"Upload vehicle #{idx} failed!")
        return True
    except:
        return False
