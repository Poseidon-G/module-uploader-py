from random import choice
from mongoengine.document import Document
from mongoengine.fields import EnumField, BooleanField, ListField,StringField, DateTimeField, DictField, IntField
from bson.objectid import ObjectId
from datetime import datetime
from enum import Enum

class StreamTypes(Enum):
    YOUTUBE = "YOUTUBE",
    RTSP = "RTSP"

class CameraInfos(Document):
    uuid = StringField(required=True, default=str(ObjectId()))
    camera_name = StringField(required=True)
    camera_url = StringField(required=True)
    type_url_stream: EnumField(StreamTypes,required= True)
    address = DictField(default = {
        "lat": 0,
        "long": 0,
        "name": ""
    })
    status = BooleanField(required=True, default=False)
    roi = ListField(ListField(IntField()), default=[], required=True)
    direction_vector = ListField(ListField(IntField()), max_length=2, default=[0,0], required=True)
    updated_at = DateTimeField(default=datetime.now)
    created_at = DateTimeField(default=datetime.now)
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(CameraInfos, self).save(*args, **kwargs)

    @staticmethod
    def getByName(camera_name: str):
        try:
            return CameraInfos.objects.get(camera_name=camera_name)
        except Exception:
            return None
