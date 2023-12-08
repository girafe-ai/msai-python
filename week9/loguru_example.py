import sys

from loguru import logger

# logger.add(sys.stdout, level="TRACE")
logger.remove(0)
logger.add(
    "loguru.json",
    level="INFO",
    mode="w",
    format="{time:MM-DD-YY at HH:MM} - {level} - {message}",
    rotation="100 KB",
    compression="zip",
    serialize=True,
)
logger.add(
    sys.stdout,
    level="TRACE",
    # colorize=True,
    # format="<green>{time:MM-DD-YY at HH:MM}</green> - <blue>{level}</blue> - <yellow>{message}</yellow>",
)


# for idx in range(100):
#     logger.info(f"Logging something {idx}")


@logger.catch
def divide(x: float, y: float) -> float:
    return x / y


divide(1, 2)
divide(1, 0)
logger.info(divide(1, 2))
