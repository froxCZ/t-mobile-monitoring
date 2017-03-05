import util

HOLIDAYS = [(1, 1),  # day, month
            (1, 1),
            (17, 4),
            (14, 4),
            (1, 5),
            (8, 5),
            (5, 7),
            (6, 7),
            (28, 9),
            (28, 10),
            (17, 11),
            (24, 12),
            (25, 12),
            (26, 12), ]

INITIAL_DATE = util.stringToDate("01.08.2016")

IGNORE_DAYS = [(24, 12), (31, 12), (1, 1)]


class DGenerator():
  def __init__(self):
    super().__init__()


