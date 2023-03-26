#!/bin/env python3
"""Start a WebMonitor that periodically downloads from a configured set
of URLs sends events to a Kafka topic, until SIGINT is received.
"""

import signal
import sys

from webevent.producer import Producer
from webevent.webmonitor import WebMonitor

MONITORED_WEBSITES = [
    ("https://example.com/", r"example"),
    ("https://google.com/", r"\(.*?www.*?robot.*?\)"),
]
LOOP_PERIOD_SECONDS = 5.0
TOPIC_NAME = "web_monitor"


def signal_handler(sig, frame):
    print("Stopping WebMonitor")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print("Starting WebMonitor")
    producer = Producer(TOPIC_NAME)
    monitor = WebMonitor(MONITORED_WEBSITES, LOOP_PERIOD_SECONDS, producer)
    monitor.run()


if __name__ == "__main__":
    main()
