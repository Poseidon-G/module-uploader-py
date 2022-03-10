from mongoengine.document import Document
from mongoengine.fields import EnumField, LongField, ListField,StringField, DateTimeField, DictField, IntField
from bson.objectid import ObjectId
from datetime import datetime
from enum import Enum

class VehicleTypes(Enum):
    CAR = "CAR"
    MOTORCYCLE = "MOTORCYCLE"
    BUS = "BUS"
    TRUCK = "TRUCK"
    BICYCLE = "BICYCLE"

class Vehicles(Document):
    uuid = StringField(required = True, default = str(ObjectId()))
    camera_uuid = StringField(required = True)
    video_id = StringField(required = True)

    vehicle_image_ids = ListField(StringField(), default = list)
    plate_image_ids = ListField(StringField(), default = list)
    preview_image_id = StringField(required = True)
    lp_labels = DictField(required=True) # Dict[str, float]: {label: score}
    vehicle_type = EnumField(VehicleTypes,required = True)
    
    record_time = DateTimeField(required= True)
    start_frame = LongField(required = True)
    end_frame = LongField(required = True)

    updated_at = DateTimeField(default=datetime.now)
    created_at = DateTimeField(default=datetime.now)
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(Vehicles, self).save(*args, **kwargs)
