from jsonschema import validate
from jsonschema.exceptions import ValidationError

from db_uploader.schema.schedule import PlateInfo


ScheduleVehicleValidation = {
    "definitions": {
        "ImageInfo": {
            "type": "object",
            "properties": {
                "asset_id": {
                    "type": "string"
                },
                "public_id": {
                    "type": "string"
                },
                "url": {
                    "type": "string"
                },
                "secure_url": {
                    "type": "string"
                },
                "format": {
                    "type": "string"
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time"
                }
            }
        },
        "PlateInfo": {
             "type": "object",
              "properties": {
                  "label": {
                      "type": "string"
                  },
                  "score": {
                      "type": "number"
                  }
              }
        }
    },
    "type": "object",
    "required": ["camera_id", "video_id"],
    "properties": {
        "camera_id": {
            "type": "string"
        },
        "video_id": {
            "type": "string"
        },
        "vehicle_images": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/ImageInfo"
            }
        },
        "plate_images": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/ImageInfo"
            }
        },
        "preview_image": {
            "$ref": "#/definitions/ImageInfo"
        },
        "lp_labels": {
            "type": "array",
              "items": {
                  "$ref": "#/definitions/PlateInfo"
              }
        },
        "vehicle_type": {
            "type": "string",
            "enum": ["Car", "Motorcycle", "Bus", "Truck", "Bicycle"]
        },
        "start_frame": {
            "type": "integer"
        },
        "end_frame": {
            "type": "integer"
        },
        "record_time": {
            "type": "string",
            "format": "date-time"
        },
    }
}
