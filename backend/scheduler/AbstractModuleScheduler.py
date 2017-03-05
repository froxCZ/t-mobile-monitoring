import abc
import logging

class AbstractModuleScheduler:
  name = ""
  @abc.abstractmethod
  def run(self):
    logging.info("running " + self.name)
    return
