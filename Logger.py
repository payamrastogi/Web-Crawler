import logging

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

def main():
    l = Logger.get_logger("Logger", logging.DEBUG)
    l.debug("test")

if __name__ == "__main__":
    main()
