from pathlib import Path

import logging

from logging.handlers import RotatingFileHandler


class LoggerService:

    _logger = None


    @classmethod
    def get_logger(cls):

        if cls._logger:

            return cls._logger

        log_folder = Path("logs")

        log_folder.mkdir(exist_ok=True)

        logger = logging.getLogger("AutoZipBackup")

        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(

            "%(asctime)s | %(levelname)s | %(message)s"

        )

        file_handler = RotatingFileHandler(

            log_folder / "autozip.log",

            maxBytes=5 * 1024 * 1024,

            backupCount=10,

            encoding="utf8"

        )

        file_handler.setFormatter(formatter)

        console = logging.StreamHandler()

        console.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.addHandler(console)

        cls._logger = logger

        return logger