import logging


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
