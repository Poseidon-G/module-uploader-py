from mongoengine.document import Document
from mongoengine.fields import EnumField, LongField, ListField,StringField, DateTimeField, DictField, IntField
from mongoengine.errors import ValidationError
from bson.objectid import ObjectId
from datetime import datetime
from enum import Enum

def _check_valid_possible_plates(input):
    #filter(@para1, @para2)
    #@para1 : func
    #@para2: interable
    print(input)
    if(
        len(list(filter(lambda element: element.__contains__('predict') and  element.__contains__('accurate'), input))) != len(input)
    ):
        raise ValidationError("invalid possible_plates_format")


class VehicleTypes(Enum):
    CAR = "CAR"
    MOTORCYCLE = "MOTORCYCLE"
    BUS = "BUS"
    TRUCK = "TRUCK"
    BICYCLE = "BICYCLE"

#old name Plate Recognize
class VehicleDetects(Document):
    uuid = StringField(required = True, default = str(ObjectId()))
    camera_uuid = StringField(required = True)
    vehicle_image_ids = ListField(StringField(), default = list)
    plate_image_ids = ListField(StringField(), default = list)
    video_id = StringField(required = True)
    record_time = DateTimeField(required= True)
    start_frame = LongField(required = True)
    end_frame = LongField(required = True)
    """
    possible_plates fields
    @input List(DictField)
    expect: [
        {
            predict: "78-H1 56434",
            accurate: 0.78
        }
    ] 
    """
    possible_plates = ListField(DictField(), default = list, validation = _check_valid_possible_plates )
    preview_image_id = StringField(required = True)
    vehicle_type = EnumField(VehicleTypes,required = True)
    updated_at = DateTimeField(default=datetime.now)
    created_at = DateTimeField(default=datetime.now)
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(VehicleDetects, self).save(*args, **kwargs)
