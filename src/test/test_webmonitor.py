from unittest import mock
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import sentinel

from webevent.webmonitor import WebMonitor


@patch('webevent.webmonitor.WebDownloader')
@patch('time.sleep')
class TestStringMethods(TestCase):

    def test_webmonitor_no_run(self, time_sleep, webdownloader):
        website_configs = []
        monitor = WebMonitor(website_configs, sentinel.loop_period, sentinel.producer)

        time_sleep.assert_not_called()


    def test_webmonitor_run_at_least_once(self, time_sleep, webdownloader):
        website_configs = []
        monitor = WebMonitor(website_configs, sentinel.loop_period, sentinel.producer)
        time_sleep.side_effect = [KeyboardInterrupt]

        with self.assertRaises(KeyboardInterrupt):
            monitor.run()

        time_sleep.assert_called_once_with(sentinel.loop_period)


    def test_webmonitor_run_until_exception_raised(self, time_sleep, webdownloader):
        website_configs = []
        monitor = WebMonitor(website_configs, sentinel.loop_period, sentinel.producer)
        time_sleep.side_effect = [None, None, KeyboardInterrupt, None]

        with self.assertRaises(KeyboardInterrupt):
            monitor.run()

        time_sleep.assert_called_with(sentinel.loop_period)
        self.assertEqual(time_sleep.call_count, 3)


    def test_webmonitor_run_produce_one_website_event(self, time_sleep, webdownloader):
        website_configs = [
            ("https://example.com/", r"example"),
        ]
        producer = mock.MagicMock()
        monitor = WebMonitor(website_configs, sentinel.loop_period, producer)
        time_sleep.side_effect = [KeyboardInterrupt]
        webdownloader.return_value.produce_event.return_value = sentinel.event

        with self.assertRaises(KeyboardInterrupt):
            monitor.run()

        time_sleep.assert_called_once_with(sentinel.loop_period)
        producer.send.assert_called_once_with(sentinel.event)


    def test_webmonitor_run_produce_one_website_event_per_config(self, time_sleep, webdownloader):
        website_configs = [
            ("https://example.com/", r"example"),
            ("https://example.com/", r"example"),
        ]
        producer = mock.MagicMock()
        monitor = WebMonitor(website_configs, sentinel.loop_period, producer)
        time_sleep.side_effect = [KeyboardInterrupt]
        webdownloader.return_value.produce_event.return_value = sentinel.event

        with self.assertRaises(KeyboardInterrupt):
            monitor.run()

        time_sleep.assert_called_once_with(sentinel.loop_period)
        producer.send.assert_called_with(sentinel.event)
        self.assertEqual(producer.send.call_count, len(website_configs))


    def test_webmonitor_run_produce_one_website_event_per_config_per_loop(self, time_sleep, webdownloader):
        website_configs = [
            ("https://example.com/", r"example"),
            ("https://example.com/", r"example"),
        ]
        producer = mock.MagicMock()
        monitor = WebMonitor(website_configs, sentinel.loop_period, producer)
        sleeps = [None, KeyboardInterrupt]
        time_sleep.side_effect = sleeps
        webdownloader.return_value.produce_event.return_value = sentinel.event

        with self.assertRaises(KeyboardInterrupt):
            monitor.run()

        time_sleep.assert_called_with(sentinel.loop_period)
        self.assertEqual(time_sleep.call_count, len(sleeps))
        producer.send.assert_called_with(sentinel.event)
        self.assertEqual(producer.send.call_count, len(website_configs) * len(sleeps))
