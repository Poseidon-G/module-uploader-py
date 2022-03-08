from mongoengine.document import Document
from mongoengine.fields import StringField, DateTimeField, IntField
from bson.objectid import ObjectId
from datetime import datetime

class RecordVideos(Document):
    uuid = StringField(required = True, default = str(ObjectId()))
    video_url = StringField(required = True)
    width = IntField(required = True)
    height = IntField(required = True)
    fps = IntField(required = True)
    num_frames = IntField(required = True)
    camera_id =  StringField(required = True)
    updated_at = DateTimeField(default=datetime.now)
    created_at = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(RecordVideos, self).save(*args, **kwargs)