from mongoengine.document import Document
from mongoengine.fields import StringField, DateTimeField
from bson.objectid import ObjectId
from datetime import datetime


class Images(Document):
  asset_id = StringField(required=True)
  public_id = StringField(required=True)
  url = StringField(required=True)
  secure_url = StringField(required=True)
  format = StringField(required=True)
  updated_at = DateTimeField(default=datetime.now)
  created_at = DateTimeField(default=datetime.now)

  def save(self, *args, **kwargs):
    if not self.created_at:
      self.created_at = datetime.now()
    self.updated_at = datetime.now()
    return super(Images, self).save(*args, **kwargs)
