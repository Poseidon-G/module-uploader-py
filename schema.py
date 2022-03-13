from dataclasses import dataclass
from os import PathLike
from datetime import datetime
from typing import List, Dict
from numpy import ndarray
from base64 import b64encode
from cv2 import imencode
from db_uploader.model.vehicle import VehicleTypes

_JPG_BASE64_HEADER="data:image/jpeg;base64,"
_JPG_EXT=".jpg"

@dataclass
class UploadImage:
    jpeg_base64: str
    folder: PathLike

    @staticmethod
    def image_base64_encode(bgr_img: ndarray):
        return _JPG_BASE64_HEADER+b64encode(imencode(_JPG_EXT, bgr_img)[1]).decode("utf-8") 

@dataclass
class UploadVehicleInfo:
    vehicle_images: List[UploadImage]
    lp_images: List[UploadImage]
    lp_labels: Dict[str, float]
    record_time: datetime
    start_frame: int
    end_frame: int
    preview_image: UploadImage
    camera_id: str
    type: VehicleTypes
