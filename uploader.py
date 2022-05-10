from typing import Dict, List

import pymongo
from jsonschema import validate
from mongoengine import connect
from mongoengine.errors import ValidationError

from db_uploader import cloudinary_upload
from db_uploader.config import DB_NAME, MONGODB_TEST_DB_URI, MONGODB_URI
from db_uploader.model.images import Images
from db_uploader.model.record_videos import RecordVideos
from db_uploader.schema import ImageInfo, UploadVehicleInfo, VehicleSchema
from db_uploader.utils import generate_collection_name_from_time
from db_uploader.validation.schedule_validation import VehicleValidation

# conn for pymongo
conn = pymongo.MongoClient(MONGODB_URI)
database = conn[DB_NAME]

# conn for mongo engine

connect(host=MONGODB_TEST_DB_URI)


def save_image(image_b64: str, link_folder: str):
  """Upload image in JPEG base 64 format to Cloudinary, then upload Image data to Mongo Db
  Return:
      (str): Document's UUID
  """
  try:
    response_image = cloudinary_upload.upload_image(image_b64, link_folder)
    image_data = ImageInfo(
        asset_id=response_image["asset_id"],
        public_id=response_image["public_id"],
        url=response_image["url"],
        secure_url=response_image["secure_url"],
        format=response_image["format"],
        created_at=response_image["created_at"]
    )

    return image_data.asDict()
  except Exception as exp:
    return None


def save_video_get_id(video_record: RecordVideos):
  try:
    video_data: RecordVideos = video_record.save()
    return video_data.id
  except ValidationError:
    raise Exception("Recorded video data format is incorrect")


def validate_vehicle_info(vehicle_info: dict, schema_validation: dict):
  try:
    validate(instance=vehicle_info, schema=schema_validation)
  except ValidationError:
    raise Exception("Format schema vehicle is incorrect")


def save_vehicle_info(vehicle_info: UploadVehicleInfo, video_id: str):
  try:
    vehicle_images: List[Dict] = []
    lp_images: List[Dict] = []

    # convert local time record video to utc time
    # vehicle_info.record_time = convertLocalTimeToUTCTime(
    #     vehicle_info.record_time)

    for vehicle_image_data in vehicle_info.vehicle_images:
      vehicle_images.append(save_image(
          vehicle_image_data.jpeg_base64, vehicle_image_data.folder))

    for lp_image_data in vehicle_info.lp_images:
      lp_images.append(save_image(
          lp_image_data.jpeg_base64, lp_image_data.folder))

    preview_image = save_image(
        vehicle_info.preview_image.jpeg_base64, vehicle_info.preview_image.folder)

    data = VehicleSchema(
        camera_id=vehicle_info.camera_id,
        vehicle_images=vehicle_images,
        plate_images=lp_images,
        video_id=video_id,
        # change to isoformat fo validate
        record_time=vehicle_info.record_time,
        start_frame=vehicle_info.start_frame,
        end_frame=vehicle_info.end_frame,
        lp_labels=vehicle_info.lp_labels,
        preview_image=preview_image,
        vehicle_type=vehicle_info.type.value,
    )

    new_vehicle = data.asDict()

    # validate data vehicle before save
    validate_vehicle_info(new_vehicle, VehicleValidation)

    # generate name collection from record_time
    schedule_vehicle_collection_name = generate_collection_name_from_time(
        vehicle_info.record_time)

    # save info to collection
    database[schedule_vehicle_collection_name].insert_one(new_vehicle)
    return True
  except ValidationError as e:
    print(e)
    return False


def upload_detected_vehicles(vehicle_data: List[UploadVehicleInfo], record_video: RecordVideos):
  try:
    video_id = str(save_video_get_id(record_video))

    for idx, data in enumerate(vehicle_data):
      flag = save_vehicle_info(data, video_id)
      if not flag:
        print(f"Upload vehicle #{idx} failed!")
    return True
  except Exception as e:
    print(e)
    return False
