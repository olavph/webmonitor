#!/bin/env python3
"""Start a WebMonitor that periodically downloads from a configured set
of URLs sends events to a Kafka topic, until SIGINT is received.
"""

import os
import signal
import sys

from webevent.producer import Producer
from webevent.webmonitor import WebMonitor

MONITORED_WEBSITES = [
    ("https://example.com/", r"example"),
    ("https://google.com/", r"\(.*?www.*?robot.*?\)"),
]
LOOP_PERIOD_SECONDS = 5.0
KAFKA_HOST=os.getenv("KAFKA_HOST", "localhost")
KAFKA_PORT=os.getenv("KAFKA_PORT", 9092)
TOPIC_NAME = "webmonitor"

def signal_handler(sig, frame):
    print("Stopping WebMonitor")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print("Starting WebMonitor")
    producer = Producer(KAFKA_HOST, KAFKA_PORT, TOPIC_NAME)
    monitor = WebMonitor(MONITORED_WEBSITES, LOOP_PERIOD_SECONDS, producer)
    monitor.run()


if __name__ == "__main__":
    main()
