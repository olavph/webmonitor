#!/bin/env python3

import signal
import sys

from webmonitor import WebMonitor

MONITORED_WEBSITES = [
    ("https://example.com/", r"example"),
    ("https://google.com/", r"\(.*?www.*?robot.*?\)"),
]
LOOP_PERIOD_SECONDS = 5.0


def signal_handler(sig, frame):
    print("Stopping WebMonitor")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    monitor = WebMonitor(MONITORED_WEBSITES, LOOP_PERIOD_SECONDS)
    monitor.run()


if __name__ == "__main__":
    main()
