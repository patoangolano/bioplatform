import logging
import os

from arq import cron, func
from arq.connections import RedisSettings

logger = logging.getLogger(__name__)

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")


async def run_analysis(ctx: dict, task_id: str) -> str:
    """Placeholder analysis task."""
    logger.info(f"Running analysis for task {task_id}")
    return f"Analysis complete for {task_id}"


class WorkerSettings:
    functions = [func(run_analysis)]
    redis_settings = RedisSettings.from_dsn(REDIS_URL)

    @staticmethod
    def on_startup(ctx: dict) -> None:
        logger.info("bioplatform-worker starting up")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Worker module loaded")
