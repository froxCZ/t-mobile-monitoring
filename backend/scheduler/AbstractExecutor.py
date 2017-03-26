import abc

import logging
import threading


class AbstractExecutor:
  name = ""

  def __init__(self, name):
    self.name = name
    pass

  def execute(self):
    try:
      logging.info(" Running " + self.name + " on thread " + str(threading.get_ident()))
      self._executeInternal()
      # todo: save success status
    except Exception as e:
      logging.exception("Executing failed.")
    return

  @abc.abstractmethod
  def _executeInternal(self):
    return
