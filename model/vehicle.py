from email.policy import default
from mongoengine.document import Document
from mongoengine.fields import EnumField, LongField, ListField,StringField, DateTimeField, DictField, ObjectIdField
from bson.objectid import ObjectId
from datetime import datetime
from enum import Enum
import time

def convertLocalTimeToUTCTime(local_time):
    epochSecond = time.mktime(local_time.timetuple())
    return datetime.utcfromtimestamp(epochSecond)

class VehicleTypes(Enum):
    CAR = "Car"
    MOTORCYCLE = "Motorcycle"
    BUS = "Bus"
    TRUCK = "Truck"
    BICYCLE = "Bicycle"

class Vehicles(Document):
    camera_id = StringField(required = True)
    video_id = StringField(required = True)

    vehicle_image_ids = ListField(ObjectIdField(), default = list)
    plate_image_ids = ListField(ObjectIdField(), default = list)
    preview_image_id = ObjectIdField(required = True)
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
