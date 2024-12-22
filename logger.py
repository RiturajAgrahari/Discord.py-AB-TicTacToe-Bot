import logging

# create logger for info and error
debug_logger = logging.getLogger("debug_logger")
info_logger = logging.getLogger("info_logger")
error_logger = logging.getLogger("error_logger")

# set up level for both loggers
debug_logger.setLevel(logging.DEBUG)
info_logger.setLevel(logging.INFO)
error_logger.setLevel(logging.ERROR)

# create file handler for different logs
debug_log = logging.FileHandler(filename="logs/debug.log", mode="w")
info_log = logging.FileHandler(filename="logs/info.log", mode="w")
error_console = logging.StreamHandler()
error_log = logging.FileHandler(filename="logs/error.log", mode="w")

# set up level for fileHandler to filter logs
debug_log.setLevel(logging.DEBUG)
info_log.setLevel(logging.INFO)
error_log.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter(' [ %(asctime)s - %(name)s - %(levelname)s ] : %(message)s')

# create console handler with a higher log level
debug_log.setFormatter(formatter)
info_log.setFormatter(formatter)
error_log.setFormatter(formatter)
error_console.setFormatter(formatter)

# add the handlers to the logger
debug_logger.addHandler(debug_log)
info_logger.addHandler(info_log)
error_logger.addHandler(error_log)
error_logger.addHandler(error_console)


def main():
    debug_logger.debug("DEBUG 0")
    info_logger.info('logging from info logger! ')
    info_logger.info('logging again from info logger! ')
    info_logger.info('logging again and again from info logger! ')
    debug_logger.debug("DEBUG 1")
    info_logger.error("this is an error")
    error_logger.error("this is an error")
    print("which log type is this?")


if __name__ == "__main__":
    main()


