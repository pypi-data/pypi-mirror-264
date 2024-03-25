"""Module for logging utilities."""

import logging
from functools import lru_cache, partial
from typing import Optional

from rich.logging import RichHandler  # type: ignore
from rich.markup import escape  # type: ignore

import astro


@lru_cache()
def get_logger(
    name: Optional[str] = None,
) -> logging.Logger:
    """
    Retrieves a logger with the given name, or the root logger if no name is given.

    Args:
        name: The name of the logger to retrieve.

    Returns:
        The logger with the given name, or the root logger if no name is given.

    Example:
        Basic Usage of `get_logger`
        ```python
        from astro.utilities.logging import get_logger

        logger = get_logger("astro.test")
        logger.info("This is a test") # Output: astro.test: This is a test

        debug_logger = get_logger("astro.debug")
        debug_logger.debug_kv("TITLE", "log message", "green")
        ```
    """
    parent_logger = logging.getLogger("astro")

    if name:
        # Append the name if given but allow explicit full names e.g. "astro.test"
        # should not become "astro.astro.test"
        if not name.startswith(parent_logger.name + "."):
            logger = parent_logger.getChild(name)
        else:
            logger = logging.getLogger(name)
    else:
        logger = parent_logger

    add_logging_methods(logger)
    return logger


def setup_logging(
    level: Optional[str] = None,
) -> None:
    logger = get_logger()

    if level is not None:
        logger.setLevel(level)
    else:
        logger.setLevel(astro.settings.log_level)

    logger.handlers.clear()

    handler = RichHandler(rich_tracebacks=True, markup=False)
    formatter = logging.Formatter("%(name)s: %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False


def add_logging_methods(logger: logging.Logger) -> None:
    def log_style(level: int, message: str, style: Optional[str] = None):
        if not style:
            style = "default on default"
        message = f"[{style}]{escape(str(message))}[/]"
        logger.log(level, message, extra={"markup": True})

    def log_kv(
        level: int,
        key: str,
        value: str,
        key_style: str = "default on default",
        value_style: str = "default on default",
        delimiter: str = ": ",
    ):
        logger.log(
            level,
            f"[{key_style}]{escape(str(key))}{delimiter}[/][{value_style}]{escape(str(value))}[/]",
            extra={"markup": True},
        )

    setattr(logger, "debug_style", partial(log_style, logging.DEBUG))
    setattr(logger, "info_style", partial(log_style, logging.INFO))
    setattr(logger, "warning_style", partial(log_style, logging.WARNING))
    setattr(logger, "error_style", partial(log_style, logging.ERROR))
    setattr(logger, "critical_style", partial(log_style, logging.CRITICAL))

    setattr(logger, "debug_kv", partial(log_kv, logging.DEBUG))
    setattr(logger, "info_kv", partial(log_kv, logging.INFO))
    setattr(logger, "warning_kv", partial(log_kv, logging.WARNING))
    setattr(logger, "error_kv", partial(log_kv, logging.ERROR))
    setattr(logger, "critical_kv", partial(log_kv, logging.CRITICAL))
