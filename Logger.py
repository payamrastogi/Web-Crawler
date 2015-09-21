import logging

"""
Used for logging, default log file path is ./log/webcrawler.log
"""
class Logger(object):
    @staticmethod
    def get_logger(class_name, log_level):
        logger = logging.getLogger(class_name)
        hdlr = logging.FileHandler("./log/webcrawler.log")
        formatter = logging.Formatter("%(asctime)-15s %(levelname)s  %(module)s.%(funcName)s(): %(message)s")
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(log_level)
        return logger

""" for testing """
def main():
    l = Logger.get_logger("Logger", logging.DEBUG)
    l.debug("test")

if __name__ == "__main__":
    main()
