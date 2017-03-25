import abc

import logging


class AbstractExecutor:
  name = ""

  def __init__(self,name):
    self.name = name
    pass

  def execute(self):
    try:
      logging.info("Running "+self.name)
      self._executeInternal()
      # todo: save success status
    except Exception as e:
      pass  # log exception
    return

  @abc.abstractmethod
  def _executeInternal(self):
    return
