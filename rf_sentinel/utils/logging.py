"""Logging estructurado."""

import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """Configura logging estructurado."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Obtiene logger con nombre de módulo."""
    return logging.getLogger(name)
