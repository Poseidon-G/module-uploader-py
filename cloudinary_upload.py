import cloudinary
from cloudinary.uploader import upload, destroy
from .config import CLOUDINARY_STORAGE

cloudinary.config(
    cloud_name=CLOUDINARY_STORAGE["CLOUD_NAME"],
    api_key=CLOUDINARY_STORAGE["API_KEY"],
    api_secret=CLOUDINARY_STORAGE["API_SECRET"]
)

#tk: luc22082000@gmail.com
# mk: Dkmconcho1
# upload image to cloudinary


def upload_image(image_base64: str, folder: str):
  return upload(image_base64, folder=folder)


def remove_image_id(_publicId):
  return destroy(_publicId)
