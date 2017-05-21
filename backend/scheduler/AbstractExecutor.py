import abc
import logging
import threading

from common import AppConfig


class AbstractExecutor:
  """
  Class which is implemented by executors performing certain task. Executed by Abstract Scheduler.
  """
  def __init__(self, name, interval):
    self.name = name
    self.interval = interval
    pass

  def execute(self):
    try:
      logging.debug(" Running " + self.name + " on thread " + str(threading.get_ident()))
      self._executeInternal()
      from common import SystemStatusManager
      SystemStatusManager.saveExecutorSuccessfulExecution(self.name, AppConfig.getCurrentTime())
    except Exception as e:
      logging.exception("Executing failed.")
    return

  @abc.abstractmethod
  def _executeInternal(self):
    return

  def getInterval(self):
    return self.interval
