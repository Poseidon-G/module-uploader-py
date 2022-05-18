from datetime import datetime
import datetime as DateTime
import time

_TYPE_COLLECTION_VEHICLE = "vehicle"


def generate_collection_name_from_time(time_record:  datetime):
  try:
    # convert to local time to easier manage
    time_record = datetime_from_utc_to_local(time_record)
    return time_record.strftime("%Y-%m-%d-%H") + "-" + _TYPE_COLLECTION_VEHICLE
  except:
    raise Exception("Cannot change date time to str")


def datetime_from_utc_to_local(utc_datetime):
  offset = DateTime.timedelta(hours=7)
  return utc_datetime + offset


def convertLocalTimeToUTCTime(local_time: datetime):
  epochSecond = time.mktime(local_time.timetuple())
  return datetime.utcfromtimestamp(epochSecond)

datetime_from_utc_to_local(datetime.now())