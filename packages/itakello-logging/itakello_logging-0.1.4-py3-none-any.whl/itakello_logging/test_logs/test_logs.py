import logging

logger = logging.getLogger(__name__)


def test_func():
    logger.debug("Test debug message from test.py")
    logger.info("Test info message from test.py")
    logger.warning("Test warning message from test.py")
    logger.error("Test error message from test.py")
    logger.critical("Test critical message from test.py")
