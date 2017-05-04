import logging

logging.getLogger().setLevel(logging.INFO)


class PrintLog:
    def out(self, name, msg):
        logging.info("~~~~, %s=%s" % (name, msg))
