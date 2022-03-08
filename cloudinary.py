import cloudinary
import cloudinary.uploader
import cloudinary.api
from config import CLOUDINARY_STORAGE

cloudinary.config( 
  cloud_name = CLOUDINARY_STORAGE["CLOUD_NAME"], 
  api_key = CLOUDINARY_STORAGE["API_KEY"], 
  api_secret = CLOUDINARY_STORAGE["API_SECRET"]
)

#tk: luc22082000@gmail.com
# mk: Dkmconcho1
#upload image to cloudinary
def upload_image(_linkImage, _folder):
  return cloudinary.uploader.upload(_linkImage, folder = _folder)

def remove_image_id(_publicId):
  return cloudinary.uploader.destroy(_publicId)


