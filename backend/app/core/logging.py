from loguru import logger

from app.core.config import settings

logger
import sys

logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL
)

logger.add(
    "logs/app.log",
    rotation="10MB",
    retention="10 days"
)

app_logger = logger