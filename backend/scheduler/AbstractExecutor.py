import abc
import logging
import threading

from config import AppConfig


class AbstractExecutor:
  def __init__(self, name):
    self.name = name
    pass

  def execute(self):
    try:
      logging.info(" Running " + self.name + " on thread " + str(threading.get_ident()))
      self._executeInternal()
      from common import SystemStatusManager
      SystemStatusManager.saveExecutorSuccessfulExecution(self.name, AppConfig.getCurrentTime())
    except Exception as e:
      logging.exception("Executing failed.")
    return

  @abc.abstractmethod
  def _executeInternal(self):
    return
