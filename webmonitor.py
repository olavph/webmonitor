import time

from webdownloader import WebDownloader

class WebMonitor:
    def __init__(self, website_configs: list, loop_period: float):
        self.downloaders = list()
        for url, regexp in website_configs:
            self.downloaders.append(WebDownloader(url, regexp))
        self.loop_period = loop_period

    def run(self):
        while(True):
            for downloader in self.downloaders:
                print(downloader.produce_event())
            time.sleep(self.loop_period)
