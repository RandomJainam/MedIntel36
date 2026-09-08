import logging
from pathlib import Path


class Logger:

    _logger = None

    @staticmethod
    def get_logger():
        if Logger._logger is not None:
            return Logger._logger

        logger = logging.getLogger("MedIntel360")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            logger.addHandler(console_handler)

        Logger._logger = logger

        return logger