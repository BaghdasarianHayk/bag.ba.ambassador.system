"""
Taskiq worker runner

Run this with the taskiq CLI:
    taskiq worker tasks:broker

Or use this script which does the same:
    python consumer.py
"""
import sys
import logging
from taskiq.cli.worker.run import run_worker_cmd

from config import configure_logging

log = logging.getLogger(__name__)


def main():
    configure_logging(level=logging.WARNING)
    log.warning("Starting taskiq worker...")
    
    # Run taskiq worker programmatically
    sys.argv = ["taskiq", "worker", "tasks:broker"]
    run_worker_cmd()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
