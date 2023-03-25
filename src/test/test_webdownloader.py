from unittest import TestCase
from unittest.mock import patch
from unittest.mock import sentinel

from webevent.webdownloader import WebDownloader
from webevent.webevent import WebEvent

@patch('requests.get')
class TestStringMethods(TestCase):

    def test_webdownloader_ok_empty_match(self, requests_get):
        expected_event = WebEvent(sentinel.url, 200, 0.1, True, "")
        requests_get.return_value.status_code = expected_event.status_code
        requests_get.return_value.elapsed.total_seconds.return_value = expected_event.response_time
        requests_get.return_value.text = ""
        downloader = WebDownloader(sentinel.url, "")

        event = downloader.produce_event()

        requests_get.assert_called_once_with(sentinel.url)
        self.assertEqual(event, expected_event)


    def test_webdownloader_ok_match(self, requests_get):
        expected_event = WebEvent(sentinel.url, 200, 0.1, True, "match")
        requests_get.return_value.status_code = expected_event.status_code
        requests_get.return_value.elapsed.total_seconds.return_value = expected_event.response_time
        requests_get.return_value.text = "The match is in the text"
        downloader = WebDownloader(sentinel.url, "match")

        event = downloader.produce_event()

        requests_get.assert_called_once_with(sentinel.url)
        self.assertEqual(event, expected_event)


    def test_webdownloader_ok_no_match(self, requests_get):
        expected_event = WebEvent(sentinel.url, 200, 0.2, False, None)
        requests_get.return_value.status_code = expected_event.status_code
        requests_get.return_value.elapsed.total_seconds.return_value = expected_event.response_time
        requests_get.return_value.text = "The match is not in the text"
        downloader = WebDownloader(sentinel.url, "no match")

        event = downloader.produce_event()

        requests_get.assert_called_once_with(sentinel.url)
        expected_event = WebEvent(sentinel.url, 200, 0.2, False, None)
        self.assertEqual(event, expected_event)


    def test_webdownloader_not_found_match(self, requests_get):
        expected_event = WebEvent(sentinel.url, 404, 0.1, True, "match")
        requests_get.return_value.status_code = expected_event.status_code
        requests_get.return_value.elapsed.total_seconds.return_value = expected_event.response_time
        requests_get.return_value.text = "The match is in the text"
        downloader = WebDownloader(sentinel.url, "match")

        event = downloader.produce_event()

        requests_get.assert_called_once_with(sentinel.url)
        self.assertEqual(event, expected_event)


    def test_webdownloader_not_found_no_match(self, requests_get):
        expected_event = WebEvent(sentinel.url, 404, 0.2, False, None)
        requests_get.return_value.status_code = expected_event.status_code
        requests_get.return_value.elapsed.total_seconds.return_value = expected_event.response_time
        requests_get.return_value.text = "The match is not in the text"
        downloader = WebDownloader(sentinel.url, "no match")

        event = downloader.produce_event()

        requests_get.assert_called_once_with(sentinel.url)
        self.assertEqual(event, expected_event)


    def test_webdownloader_ok_regexp_match(self, requests_get):
        expected_event = WebEvent(sentinel.url, 200, 0.1, True, "very.\n complex\n. The match")
        requests_get.return_value.status_code = expected_event.status_code
        requests_get.return_value.elapsed.total_seconds.return_value = expected_event.response_time
        requests_get.return_value.text = "very.\n complex\n. The match is somewhere in the text"
        downloader = WebDownloader(sentinel.url, "very.*complex.*match")

        event = downloader.produce_event()

        requests_get.assert_called_once_with(sentinel.url)
        self.assertEqual(event, expected_event)
