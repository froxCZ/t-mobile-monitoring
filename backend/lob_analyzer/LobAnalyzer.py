import logging

from config import config


class LobAnalyzer:
  def __init__(self,flow):
    super().__init__()
    self.flow = flow

  def run(self):
    logging.info("analyzing " + self.flow["name"])



    return 0

  def getResult(self):
    """
    returns result. It's up to caller to save it to db!
    :return:
    """
    pass


if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s [%(module)s]: %(message)s', level=logging.DEBUG)
  gsm = config.getLobConfig("CZ_GSM")
  LobAnalyzer(gsm["flows"]["MSSCEB1B"]).run()