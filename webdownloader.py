import re
import requests

class WebDownloader:
    def __init__(self, url: str, regexp_pattern: str):
        self.url = url
        self.regexp = re.compile(regexp_pattern)

    def produce_event(self):
        response = requests.get(self.url)
        status_code = response.status_code
        elapsed_time = response.elapsed.total_seconds()
        regexp_match = self.regexp.search(response.text)
        return (f"URL: {self.url}, "
                f"status code: {status_code}, "
                f"response time: {elapsed_time:.3f}, "
                f"regexp match found: {regexp_match is not None}, "
                f"regexp match: {regexp_match and regexp_match.group(0)}")
