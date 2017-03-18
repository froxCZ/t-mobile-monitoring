import abc


class AbstractAnalyzerRunner:
  name = ""

  def __init__(self):
    pass

  def run(self):
    try:
      self._runInternal()
      # save success status
    except Exception as e:
      pass  # log exception
    return

  @abc.abstractmethod
  def _runInternal(self):
    return
