from core.utils import query_live_urls, query_device_code, get_video_urls, gen_time, start_live, get_live_urls, download_m3u8_video


class Room:
    def __init__(self, building_num, room_num):
        self.building_num = building_num
        self.room_num = room_num
        self.device_code = query_device_code([building_num, room_num])

    def get_live_urls(self):
        urls = get_live_urls(self.device_code)
        return urls

    def query_live_urls(self):
        urls = query_live_urls(self.device_code)
        self.live_urls = urls
        return urls

    def get_video_urls(self, time_data):
        start_time, end_time = gen_time(time_data['year'], time_data['month'], time_data['day'], time_data['course'])
        urls = get_video_urls(self.device_code, start_time, end_time)
        self.video_urls = urls
        return urls

    def start_live(self, type_num):
        types = ['teacherFull', 'teacherTrack', 'pptVideo', 'studentFull', 'mobile']
        thistype = types[type_num]
        start_live(self.live_urls[thistype])

    def download_m3u8_video(self, type_num, outfile_name):
        types = ['teacherFull', 'teacherTrack', 'pptVideo', 'studentFull', 'mobile']
        thistype = types[type_num]
        download_m3u8_video(self.video_urls[thistype], outfile_name)
