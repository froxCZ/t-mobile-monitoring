import abc


class AbstractModuleScheduler:

  def __init__(self):
    pass


  name = ""
  @abc.abstractmethod
  def run(self):
    return
