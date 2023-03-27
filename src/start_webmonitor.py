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
TOPIC_NAME = "webmonitor"
KAFKA_HOST=os.getenv("KAFKA_HOST", "localhost")
KAFKA_PORT=os.getenv("KAFKA_PORT", 9092)
KAFKA_SECURITY_PROTOCOL=os.getenv("KAFKA_SECURITY_PROTOCOL", "PLAINTEXT")
KAFKA_SSL_CAFILE=os.getenv("KAFKA_SSL_CAFILE", None)
KAFKA_SSL_CERTFILE=os.getenv("KAFKA_SSL_CERTFILE", None)
KAFKA_SSL_KEYFILE=os.getenv("KAFKA_SSL_KEYFILE", None)


def signal_handler(sig, frame):
    print("Stopping WebMonitor")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print("Starting WebMonitor")
    producer = Producer(TOPIC_NAME, KAFKA_HOST, KAFKA_PORT,
                        security_protocol=KAFKA_SECURITY_PROTOCOL,
                        ssl_cafile=KAFKA_SSL_CAFILE,
                        ssl_certfile=KAFKA_SSL_CERTFILE,
                        ssl_keyfile=KAFKA_SSL_KEYFILE,
    )
    monitor = WebMonitor(MONITORED_WEBSITES, LOOP_PERIOD_SECONDS, producer)
    monitor.run()


if __name__ == "__main__":
    main()
