import requests
import time
import json
import urllib.parse as parse
import os
from config import base_path

device_code_file_path = base_path + '/data/devices.json'
urls_file_path = base_path + '/data/urls.json'
cache_file_path = base_path + '/data/cache.json'


def get_device_code():
    try:
        url = 'http://newesxidian.chaoxing.com/live/listSignleCourse'

        with open(cache_file_path) as f:
            cache = json.load(f)

        i = int(cache["i"])

        with open(device_code_file_path) as f:
            try:
                deviceData = json.load(f)
            except json.decoder.JSONDecodeError:
                deviceData = {}

        while (i <= 10700000):
            print(i)
            liveId = i
            data = {
                'liveId': liveId,
                'fid': '16820'
            }
            post = requests.post(url, data=data)
            try:
                schoolRoomCode = post.json()[0]['schoolRoomCode']
                deviceCode = post.json()[0]['deviceCode']
                print(schoolRoomCode + ':' + deviceCode)

                deviceData[schoolRoomCode] = deviceCode

            except IndexError:
                i += 5
                continue
            i += 5
            time.sleep(0.2)

    except KeyboardInterrupt or Exception:
        cache['i'] = i
        with open(cache_file_path, 'w') as f:
            f.write(json.dumps(cache, ensure_ascii=False))

        with open(device_code_file_path, 'w') as f:
            f.write(json.dumps(deviceData, ensure_ascii=False))
    else:
        cache['i'] = i
        with open(cache_file_path, 'w') as f:
            f.write(json.dumps(cache, ensure_ascii=False))

        with open(device_code_file_path, 'w') as f:
            f.write(json.dumps(deviceData, ensure_ascii=False))


def add_device_code(building_num, room_num, device_code):
    pass


def download_m3u8_video(url, output_filename):
    from core.m3u8_downloader import Downloader
    a = Downloader(50)
    a.run(url, output_filename)


def gen_time(year, month, day, course):
    this_day = '{}-{}-{}'.format(year, month, day)

    time = {
        '1': {
            'start_time': this_day + ' ' + '08:30:00.0',
            'end_time': this_day + ' ' + '09:15:00.0',
        },
        '2': {
            'start_time': this_day + ' ' + '09:20:00.0',
            'end_time': this_day + ' ' + '10:05:00.0',
        },
        '3': {
            'start_time': this_day + ' ' + '10:05:00.0',
            'end_time': this_day + ' ' + '11:10:00.0',
        },
        '4': {
            'start_time': this_day + ' ' + '11:10:00.0',
            'end_time': this_day + ' ' + '12:10:00.0',
        },
        '5': {
            'start_time': this_day + ' ' + '14:00:00.0',
            'end_time': this_day + ' ' + '14:45:00.0',
        },
        '6': {
            'start_time': this_day + ' ' + '14:45:00.0',
            'end_time': this_day + ' ' + '15:40:00.0',
        },
        '7': {
            'start_time': this_day + ' ' + '15:40:00.0',
            'end_time': this_day + ' ' + '16:40:00.0',
        },
        '8': {
            'start_time': this_day + ' ' + '16:40:00.0',
            'end_time': this_day + ' ' + '17:40:00.0',
        },
        '9': {
            'start_time': this_day + ' ' + '19:00:00.0',
            'end_time': this_day + ' ' + '19:50:00.0',
        },
        '10': {
            'start_time': this_day + ' ' + '19:40:00.0',
            'end_time': this_day + ' ' + '20:40:00.0',
        }
    }

    start_time = time[course]['start_time']
    end_time = time[course]['end_time']

    return start_time, end_time


def get_live_urls(deviceCode):
    url = "http://newesxidian.chaoxing.com/live/getViewUrlNoCourseLive"
    data = {
        "deviceCode": deviceCode,
        "status": "1",
        "fid": "16820"
    }
    url = requests.post(url, data).text
    info = url.split('?')[1].split("=")[1]
    info = parse.unquote(info, encoding='utf-8', errors='replace')
    info = json.loads(info)
    return info['videoPath']


def get_video_urls(deviceCode, startTime, endTime):
    url = "http://newesxidian.chaoxing.com/live/getViewUrlNoCourseLive"
    data = {
        "deviceCode": deviceCode,
        "status": "2",
        "fid": "16820",
        "startTime": startTime,
        "endTime": endTime
    }

    url = requests.post(url, data).text
    info = url.split('?')[1].split("=")[1]
    info = parse.unquote(info, encoding='utf-8', errors='replace')
    info = json.loads(info)
    try:
        videoPath = info['videoPath']
    except Exception as e:
        videoPath = ""

    return videoPath


def check_keyword(data, keywords):
    for keyword in keywords:
        if keyword in data:
            continue
        else:
            return False
    return True


def query_device_code(keyword):
    with open(device_code_file_path) as devices_file:
        devices = json.load(devices_file)

    roomCodeList = sorted(devices)
    for room_code in roomCodeList:
        if check_keyword(room_code, keyword):
            return devices[room_code]

    return False


def query_live_urls(device_code):
    with open(urls_file_path) as url_file:
        urls = json.load(url_file)

    if device_code:
        url = urls[device_code]
        info = parse.parse_qs(url.split("?")[-1], encoding="utf-8")["info"][0]
        info = json.loads(info)
        urls = info["videoPath"]
        return urls
    else:
        return None


def start_live(url):
    cmd = "ffplay" + " " + "\"" + url + "\""
    os.system(cmd)


if __name__ == '__main__':
    get_device_code()
