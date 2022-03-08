from mongoengine import connect
import config
connect(host=config.MONGODB_URI)
import cloudinary

from model.camera_info import CameraInfos
from model.images import Images
from model.record_videos import RecordVideos
from model.vehicle_detects import VehicleDetects

def save_image_get_uuid(image, link_folder):
    try:
        response_image = cloudinary.upload_image(image, link_folder)
        image_data = Images(
            asset_id = response_image["asset_id"],
            public_id = response_image["public_id"],
            url = response_image["url"],
            secure_url = response_image["secure_url"],
            format = response_image["format"]
        ).save()
        
        return str(image_data.uuid)
    except Exception as e: 
        print(e)
        print("upload failed")



def save_video_get_uuid(video_record):
    try:
        
        video_data = RecordVideos(
            video_url = video_record["video_url"],
            width = video_record["width"],
            height = video_record["height"],
            fps = video_record["fps"],
            num_frames = video_record["num_frames"],
            camera_id =  video_record["camera_id"]
        ).save()

        return str(video_data.uuid)
    except:
        print("video failed")


def save_vehicle_detect(plate_recognize, video_id):
    try:
        list_vehicle_id_images = []
        list_plate_id_images = []

        for vehicle in plate_recognize["list_vehicle_images"]:
            list_vehicle_id_images.append(save_image_get_uuid(vehicle["image"], vehicle["folder"]))

        for plate in plate_recognize["list_plate_images"]:
            list_plate_id_images.append(save_image_get_uuid(plate["image"], plate["folder"]))
        

        preview_image_id  = save_image_get_uuid(plate_recognize["preview_image"]["image"], plate_recognize["preview_image"]["folder"])
        
        data = VehicleDetects(
            camera_uuid = plate_recognize["camera_id"],
            vehicle_image_ids = list_vehicle_id_images,
            plate_image_ids = list_plate_id_images,
            video_id = video_id,
            record_time = plate_recognize["record_time"],
            start_frame = plate_recognize["start_frame"],
            end_frame = plate_recognize["end_frame"],
            possible_plates = plate_recognize["possible_plates"],
            preview_image_id = preview_image_id,
            vehicle_type = plate_recognize["vehicle_type"]
        )
        data.save()
        print("upload save_vehicle_detect success")
    except Exception as e: 
        print(e)
        print("fail upload save_vehicle_detect")

def upload_list_vehicle_detect(list_upload, record_video):
    try:
        video_uuid = save_video_get_uuid(record_video)

        for vehicle_id in list_upload.keys():
            save_vehicle_detect(list_upload[vehicle_id], video_uuid)

        print("upload list_vehicle_detect success")
    except:
        print("upload list_vehicle_detect failed")

