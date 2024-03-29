
import logging

class SyncariLogger:
    """
        Syncari specific logger to log all messages and errors.
    """

    @staticmethod
    def get_logger(logger_name):
        """
            get logger with Syncari specific configuration.
            TODO: add syncariid/syncrunid to this.
        """
        logger = logging.getLogger(name=logger_name)
        while logger.hasHandlers():
            logger.removeHandler(logger.handlers[0])
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
