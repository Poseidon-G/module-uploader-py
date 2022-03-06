video_url = "thcstanxuan-2021-11-23-09h43m22s-09h48m22s"
import datetime
import re


def parse_hour(time): 
    _start_time = re.sub('[hms]', "-", time).split("-")
    _start_time.pop()
    return list(map(int, _start_time))


def parse_url_video(url):
    input_url = url.split("-")
    out_camera_name = input_url[0]
    input_date = list(map(int, input_url[1: 4]))
    input_start_time = parse_hour(input_url[4])
    input_end_time = parse_hour(input_url[5])

    out_start_time = datetime.datetime(input_date[0],input_date[1],input_date[2],input_start_time[0], input_start_time[1], input_start_time[2])
    out_end_time = datetime.datetime(input_date[0],input_date[1],input_date[2],input_end_time[0], input_end_time[1], input_end_time[2])
    return [out_camera_name, out_start_time, out_end_time]


print(parse_url_video(video_url))