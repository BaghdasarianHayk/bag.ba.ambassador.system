import logging
from config import configure_logging

log = logging.getLogger(__name__)


def main():
    configure_logging(level=logging.WARNING)
    
    # Import broker after logging is configured
    from tasks import broker
    
    log.warning("Starting taskiq worker...")
    broker.run_worker()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("Bye!")
