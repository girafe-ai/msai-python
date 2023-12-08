import logging

# # Different handlers
# logger = logging.getLogger(__name__)

# handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
# logger.addHandler(handler)

# handler = logging.FileHandler("logging_example.log")
# handler.setFormatter(logging.Formatter("[%(asctime)s - %(levelname)s]: %(message)s"))
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)

# handler = logging.FileHandler("critical.log")
# handler.setFormatter(logging.Formatter("[%(asctime)s]: %(message)s"))


# # Filtering
# # Take all the messages that have a word "HELP" in them
# def filter_func(record: logging.LogRecord) -> bool:
#     return record.getMessage().find("HELP") != -1


# logger.addFilter(filter_func)

# logger.debug("A DEBUG MESSAGE")
# logger.info("AN INFO MESSAGE")
# logger.warning("A HELP WARNING MESSAGE")
# logger.error("AN ERROR MESSAGE")
# logger.critical("A CRITICAL MESSAGE")


# # Adapter example
logger = logging.getLogger(__name__)


class CustomLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f'{msg} from {kwargs["extra"]["username"]}', kwargs


adapter = CustomLoggerAdapter(logger, {"username": "John"})

adapter.debug("A DEBUG MESSAGE", extra={"username": "Jane"})
adapter.info("AN INFO MESSAGE", extra={"username": "Jane"})
adapter.warning("A WARNING MESSAGE", extra={"username": "Alex"})
adapter.error("AN ERROR MESSAGE", extra={"username": "Alice"})
adapter.critical("A CRITICAL MESSAGE", extra={"username": "Bob"})
