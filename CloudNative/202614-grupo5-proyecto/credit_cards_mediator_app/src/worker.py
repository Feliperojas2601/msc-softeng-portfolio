import logging
import signal
import time

from handler import PollingError, Settings, run_once

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 2


class _Shutdown:
    def __init__(self):
        self.requested = False

    def request(self, signum, frame):
        self.requested = True


def run_forever(
    settings: Settings | None = None, *, sleep_fn=time.sleep, stop_check=None
):
    settings = settings or Settings.from_env()
    if stop_check is None:
        shutdown = _Shutdown()
        signal.signal(signal.SIGTERM, shutdown.request)
        signal.signal(signal.SIGINT, shutdown.request)
        stop_check = lambda: shutdown.requested

    logger.info("credit_cards_mediator worker started")
    while not stop_check():
        try:
            run_once(settings)
        except PollingError as error:
            logger.warning("Verification cycle failed: %s", type(error).__name__)
        sleep_fn(POLL_INTERVAL_SECONDS)
    logger.info("credit_cards_mediator worker stopped")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_forever()
