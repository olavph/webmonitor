import time

from webevent.producer import Producer
from webevent.webdownloader import WebDownloader


class WebMonitor:
    def __init__(self, website_configs: list, loop_period: float, producer: Producer):
        self.downloaders = list()
        for url, regexp in website_configs:
            self.downloaders.append(WebDownloader(url, regexp))
        self.loop_period = loop_period
        self.producer = producer

    def run(self):
        while(True):
            for downloader in self.downloaders:
                event = downloader.produce_event()
                print(event)
                self.producer.send(event)
            time.sleep(self.loop_period)
