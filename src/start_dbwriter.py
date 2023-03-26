#!/bin/env python3
"""Start a DBWriter that receives events from a Kafka topic and writes
them to a PostgresSQL, until SIGINT is received.
"""

import signal
import sys

from webevent.consumer import Consumer
from webevent.dbwriter import DBWriter
from webevent.webevent import WebEvent

TOPIC_NAME = "web_monitor"
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_NAME = "webmonitor"
TABLE_NAME = "web_events"


def signal_handler(sig, frame):
    print("Stopping DBWriter")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print("Starting DBWriter")
    consumer = Consumer(TOPIC_NAME)
    writer = DBWriter(consumer, DB_HOST, DB_PORT, DB_USER, DB_NAME, TABLE_NAME, WebEvent)
    writer.run()


if __name__ == "__main__":
    main()
