#!/bin/env python3

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
    producer = Producer(TOPIC_NAME)
    monitor = WebMonitor(MONITORED_WEBSITES, LOOP_PERIOD_SECONDS, producer)
    monitor.run()


if __name__ == "__main__":
    main()
