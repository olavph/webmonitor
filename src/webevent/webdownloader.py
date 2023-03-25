import re
import requests

from webevent.webevent import WebEvent


class WebDownloader:
    def __init__(self, url: str, regexp_pattern: str):
        self.url = url
        self.regexp = re.compile(regexp_pattern, re.MULTILINE | re.DOTALL)

    def produce_event(self):
        response = requests.get(self.url)
        status_code = response.status_code
        elapsed_time = response.elapsed.total_seconds()
        regexp_match = self.regexp.search(response.text)
        return WebEvent(self.url,
                        status_code,
                        elapsed_time,
                        regexp_match is not None,
                        regexp_match and regexp_match.group(0))
