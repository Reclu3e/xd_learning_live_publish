import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


if __name__ == '__main__':
    from core.room import Room
    
    room = Room("B", "203")

    data = {
        "year": "2022",
        "month": "04",
        "day": "07",
        "course": "7"
    }
    a = room.get_video_urls(data)
    print(a)
    room.download_m3u8_video(4, "2022-04-07-7.ts")