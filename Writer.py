class Writer(object):

    def __init__(self, base_path, log_level):
        self.base_path = base_path
        self.__setup_logging(log_level)

    def __setup_logging(self, level):
        logger = logging.getLogger("Writer")
        hdlr = logging.FileHandler("./log/webcrawler.log")
        formatter = logging.Formatter("%(asctime)-15s %(levelname)s  %(module)s.%(funcName)s(): %(message)s")
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(level)
        self.logger = logger

    def write(self, filename, text):
        f = open(base_path+filename, 'w')
        f.write(text)
        f.close()
