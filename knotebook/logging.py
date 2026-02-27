from logging import (
    Formatter,
    LogRecord, 
    Logger,
    StreamHandler,
    getLogger,
    DEBUG, INFO, WARNING, ERROR, CRITICAL,
)
from typing import Final


class LogFormatter(Formatter):
    __COLORS: Final[dict[int, str]] = {
        DEBUG: '\x1b[34m',      # Blue
        INFO: '\x1b[32m',       # Green
        WARNING: '\x1b[33m',    # Yellow
        ERROR: '\x1b[31m',      # Red
        CRITICAL: '\x1b[41m',   # Red background
    }
    __RESET: Final[str] = '\x1b[0m'


    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None
    ):
        super().__init__(fmt, datefmt)


    def format(self, record: LogRecord) -> str:
        record.levelname = f'{self.__COLORS[record.levelno]}{record.levelname}{self.__RESET}'
        return super().format(record)


logger: Logger = getLogger(__name__)
logger.setLevel(DEBUG)

stream_handler: StreamHandler = StreamHandler()
stream_handler.setFormatter(
    LogFormatter(
        fmt='%(levelname)s — [%(asctime)s] %(message)s',
        datefmt='%H:%M:%S'
    )
)

logger.addHandler(stream_handler)
