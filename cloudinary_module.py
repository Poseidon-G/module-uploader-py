import cloudinary
import cloudinary.uploader
import cloudinary.api
import config

cloudinary.config( 
  cloud_name = config.CLOUDINARY_STORAGE["CLOUD_NAME"], 
  api_key = config.CLOUDINARY_STORAGE["API_KEY"], 
  api_secret = config.CLOUDINARY_STORAGE["API_SECRET"]
)



#tk: luc22082000@gmail.com
# mk: Dkmconcho1
#
#
#upload image to cloudinary
def upload_image(_linkImage, _folder):
  return cloudinary.uploader.upload(_linkImage, folder = _folder)

def remove_image_id(_publicId):
  return cloudinary.uploader.destroy(_publicId)


