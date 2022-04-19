from email.policy import default
from mongoengine.document import Document
from mongoengine.fields import EnumField, LongField, ListField,StringField, DateTimeField, DictField
from mongoengine.errors import ValidationError
from bson.objectid import ObjectId
from datetime import datetime
from enum import Enum
import time

_MAX_SIZE_IMAGES = 2

def convertLocalTimeToUTCTime(local_time):
    epochSecond = time.mktime(local_time.timetuple())
    return datetime.utcfromtimestamp(epochSecond)

class VehicleTypes(Enum):
    CAR = "Car"
    MOTORCYCLE = "Motorcycle"
    BUS = "Bus"
    TRUCK = "Truck"
    BICYCLE = "Bicycle"

def RetrictLengthMaxLengthImage(list_image):
    if(len(list_image) > _MAX_SIZE_IMAGES):
        raise ValidationError("List images exceed max size: ", _MAX_SIZE_IMAGES) 

class NameCollection:
    name = str

class Vehicles(Document, NameCollection):
    meta = { "collection": NameCollection.name}
    camera_id = StringField(required = True)
    video_id = StringField(required = True)

    vehicle_images= ListField(DictField(), required = True, validation = RetrictLengthMaxLengthImage) #[ImageInfo]
    plate_images = ListField(DictField(), default = [], validation = RetrictLengthMaxLengthImage) #[ImageInfo]
    preview_image = DictField(required = True) #ImageInfo
    lp_labels = ListField(DictField(), default=[], requrired=True) # [{label: str, score:float}]
    vehicle_type = EnumField(VehicleTypes,required = True)
    
    record_time = DateTimeField(required= True)
    start_frame = LongField(required = True)
    end_frame = LongField(required = True)

    updated_at = DateTimeField(default=datetime.now)
    created_at = DateTimeField(default=datetime.now)
    def save(self, *args, **kwargs):
        if self.record_time:
            self.record_time = convertLocalTimeToUTCTime(self.record_time)
            
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(Vehicles, self).save(*args, **kwargs)
