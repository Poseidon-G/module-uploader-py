from cProfile import label
from dataclasses import dataclass, field
from os import PathLike
from datetime import datetime
import string
from typing import List, Dict
from numpy import ndarray
from base64 import b64encode
from cv2 import imencode
from enum import Enum


class VehicleTypes(Enum):
    CAR = "Car"
    MOTORCYCLE = "Motorcycle"
    BUS = "Bus"
    TRUCK = "Truck"
    BICYCLE = "Bicycle"


_JPG_BASE64_HEADER = "data:image/jpeg;base64,"
_JPG_EXT = ".jpg"


@dataclass
class UploadImage:
  jpeg_base64: str
  folder: PathLike

  @staticmethod
  def image_base64_encode(bgr_img: ndarray):
    return _JPG_BASE64_HEADER+b64encode(imencode(_JPG_EXT, bgr_img)[1]).decode("utf-8")


@dataclass
class ImageInfo:
  asset_id: str
  public_id: str
  url: str
  secure_url: str
  format: str
  created_at: datetime

  def asDict(self):
    return vars(self)


@dataclass
class PlateInfo:
  label: str
  score: float
  def asDict(self):
    return vars(self)

@dataclass
class UploadVehicleInfo:
  vehicle_images: List[UploadImage]
  lp_images: List[UploadImage]
  lp_labels: List[PlateInfo]  # [{label: str, score: float}]
  record_time: datetime
  start_frame: int
  end_frame: int
  preview_image: UploadImage
  camera_id: str
  type: VehicleTypes


@dataclass
class ScheduleVehicleSchema:
  record_time: datetime
  start_frame: int
  end_frame: int
  camera_id: str
  video_id: str
  vehicle_type: VehicleTypes
  preview_image: Dict #ImageInfo as dict
  vehicle_images: List[Dict] = field(default_factory=list) #ImageInfo as dict
  plate_images: List[Dict] = field(default_factory=list) #ImageInfo as dict
  lp_labels: List[Dict] = field(default_factory=list)  #PlateInfo as dict
  def asDict(self):
    return vars(self)