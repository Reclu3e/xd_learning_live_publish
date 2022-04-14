from gevent import monkey
monkey.patch_all()
import m3u8
import re
import os
from gevent.pool import Pool
import requests
import requests.adapters
import time


class Downloader:
    def __init__(self, pool_size, retry=3):
        self.pool = Pool(pool_size)
        self.sess = self._get_http_session(pool_size, pool_size, retry)
        self.retry = retry
        self.dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../download_video/video")
        self.succeed = {}
        self.failed = []
        self.ts_total = 0
        self.outfile_name = ''

    def _get_http_session(self, pool_connections, pool_maxsize, max_retries):
        sess = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=pool_connections, pool_maxsize=pool_maxsize,
                                                max_retries=max_retries)
        sess.mount('http://', adapter)
        sess.mount('https://', adapter)
        return sess

    def _download(self, ts_list):
        self.pool.map(self._worker, ts_list)
        if self.failed:
            ts_list = self.failed
            self.failed = []
            self._download(ts_list)

    def _worker(self, ts_tuple):
        url = ts_tuple[0]
        index = ts_tuple[1]
        r = self.sess.get(url, timeout=20)
        if r.ok:
            file_name = url.split('/')[-1].split('?')[0]
            file_path = os.path.join(self.dir, file_name)
            with open(file_path, 'wb') as f:
                f.write(r.content)
            self.succeed[index] = file_name
            return

        self.failed.append((url, index))

    def _join_file(self):
        outfile_path = os.path.join(self.dir, self.outfile_name)

        with open(outfile_path, "wb") as outfile:
            for index in range(0, self.ts_total):
                file_name = self.succeed.get(index, '')
                if file_name:
                    with open(os.path.join(self.dir, file_name), 'rb') as infile:
                        outfile.write(infile.read())
                    os.remove(os.path.join(self.dir, file_name))
                else:
                    time.sleep(1)

    def run(self, m3u8_url, outfile_name):
        self.outfile_name = outfile_name

        if self.dir and not os.path.isdir(self.dir):
            os.makedirs(self.dir)

        r = self.sess.get(m3u8_url, timeout=10)
        if r.ok:
            body = r.content
            if body:
                base_url = re.findall("(.*)playback\.m3u8", m3u8_url)
                playlist = m3u8.load(m3u8_url)
                ts_list = []
                for segment in playlist.segments:
                    url = base_url[0] + segment.uri
                    ts_list.append(url)

                ts_list = list(zip(ts_list, [n for n in range(len(ts_list))]))
                if ts_list:
                    self.ts_total = len(ts_list)
                    print(self.ts_total)
                    self._download(ts_list)
        else:
            print(r.status_code)

        self._join_file()

        print(self.failed)


if __name__ == '__main__':
    pass