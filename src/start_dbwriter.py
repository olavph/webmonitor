#!/bin/env python3

import signal
import sys

from webevent.dbwriter import DBWriter
from webevent.webevent import WebEvent

TOPIC_NAME = "web_monitor"
DB_NAME = "mydb"
TABLE_NAME = "web_events"


def signal_handler(sig, frame):
    print("Stopping DBWriter")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    writer = DBWriter(TOPIC_NAME, DB_NAME, TABLE_NAME, WebEvent)
    writer.run()


if __name__ == "__main__":
    main()
