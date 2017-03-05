import threading

import time


class Analyzer(threading.Thread):
  def run(self):
    while True:
      print(str(threading.get_ident()) + " a")
      time.sleep(3)


def main():
  threads = [
    Analyzer(), Analyzer(), Analyzer()
  ]

  for t in threads:
    t.start()

  time.sleep(10)
  print("x")


main()
