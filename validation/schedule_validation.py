from jsonschema import validate
from jsonschema.exceptions import ValidationError

from db_uploader.schema import PlateInfo

VehicleValidation = {
    "$jsonSchema": {
        "definitions": {
            "ImageInfo": {
                "bsonType": "object",
                "properties": {
                    "asset_id": {
                        "bsonType": "string"
                    },
                    "public_id": {
                        "bsonType": "string"
                    },
                    "url": {
                        "bsonType": "string"
                    },
                    "secure_url": {
                        "bsonType": "string"
                    },
                    "format": {
                        "bsonType": "string"
                    },
                    "created_at": {
                        "bsonType": "date",
                    }

                }
            },
            "PlateInfo": {
                "bsonType": "object",
                "properties": {
                    "label": {
                        "bsonType": "string"
                    },
                    "score": {
                        "bsonType": "number"
                    }
                }
            }
        },
        "bsonType": "object",
        "required": ["recordtime", "camera_id", "video_id", "preview_image", "start_frame", "end_frame"],
        "properties": {
            "camera_id": {
                "bsonType": "string",
                "description": "must be a string of objectId and is required"
            },
            "video_id": {
                "bsonType": "string",
                "description": "must be a string of objectId and is required"
            },
            "preview_image": {
                "$ref": "#/definitions/ImageInfo",
                "description": "must be a object ImageInfo"
            },
            "lp_labels":  {
                "bsonType": "array",
                "items": {
                    "$ref": "#/definitions/PlateInfo"
                },
                "description": "must be a array object PlateInfo"
            },
            "vehicle_type": {
                "bsonType": "string",
                "enum": ["Car", "Motorcycle", "Bus", "Truck", "Bicycle"]
            },
            "start_frame": {
                "bsonType": "number"
            },
            "end_frame": {
                "bsonType": "number"
            },
            "vehicle_images": {
                "bsonType": "array",
                "items": {
                    "$ref": "#/definitions/ImageInfo"
                },
                "description": "must be a array object ImageInfo"
            },
            "plate_images": {
                "bsonType": "array",
                "items": {
                    "$ref": "#/definitions/ImageInfo"
                },
                "description": "must be a array object ImageInfo"

            },
        }
    }
}
