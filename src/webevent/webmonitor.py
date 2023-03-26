import time

from webevent.producer import Producer
from webevent.webdownloader import WebDownloader


class WebMonitor:
    """WebMonitor periodically downloads from every listed website, producing a stream of events
    """

    def __init__(self, website_configs: list, loop_period: float, producer: Producer):
        """Initialize WebDownloaders for each listed website configuration

        Args:
            website_configs (list): list of (URL, regexp) pairs
            loop_period (float): loop period in seconds to execute download requests
            producer (Producer): sender of events
        """
        self.downloaders = list()
        for url, regexp in website_configs:
            self.downloaders.append(WebDownloader(url, regexp))
        self.loop_period = loop_period
        self.producer = producer

    def run(self):
        """Loop until interrupted, requesting information for every website in each iteration
        """
        while(True):
            for downloader in self.downloaders:
                event = downloader.produce_event()
                print(event)
                self.producer.send(event)
            self.producer.flush()
            time.sleep(self.loop_period)
