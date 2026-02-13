import sys
from pathlib import Path
from loguru import logger


class LoggerSetup:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoggerSetup, cls).__new__(cls)    
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        
        self._initialized = True
        self.log_path = Path("logs")
        self.log_path.mkdir(exist_ok=True)
        
        self._configure_logger()
    
    def _configure_logger(self):
        logger.remove()

        logger.add(
            sys.stdout,
            colorize=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="DEBUG"
        )

        logger.add(
            self.log_path / "bot.log",
            rotation="10 MB",
            retention="10 days",
            compression="zip",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
        )

        logger.add(
            self.log_path / "errors.json",
            serialize=True,
            level="ERROR",
            rotation="5 MB"
        )

    @staticmethod
    def get_logger():
        return logger
    
_setup = LoggerSetup()
app_logger = _setup.get_logger()