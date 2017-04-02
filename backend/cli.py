import argparse

from mediation.data_receiver import DataInsertor

ALLOWED_INSERTS = {"inputs", "forwards"}
ALLOWED_COUNTRY = {"CZ", "AT", "DE", "NL"}


class ParsingException(RuntimeError):
  def __init__(self, msg):
    self.msg = msg


class Cli:
  def __init__(self):
    parser = argparse.ArgumentParser(description='Mediation cli')
    parser.add_argument('--insert', help='inputs | forwards')
    parser.add_argument('--file', help='filepath')
    parser.add_argument('--dir', help='dir')
    parser.add_argument('--country', help='country')
    self.parser = parser

  def parse(self, arguments=None):
    self.args = self.parser.parse_args(arguments)
    try:
      if (self.args.insert is not None):
        self.executeInsertAction()
    except ParsingException as e:
      print('There was a parsing error: %s' % e.msg)

  def executeInsertAction(self):
    type = self.args.insert
    country = self.args.country
    if type not in ALLOWED_INSERTS:
      raise ParsingException("unknown insert type " + type)
    if country not in ALLOWED_COUNTRY:
      raise ParsingException("unknown country " + country)
    if self.args.dir is None and self.args.file is None:
      raise ParsingException("specify file or dir")
    if self.args.dir is not None:
      DataInsertor().insertDir(self.args.dir, type, country)
    else:
      DataInsertor().insertFile(self.args.file, type, country)


Cli().parse(["--insert", "inputs", "--dir", "/home/frox/tmobile/data_mar12/preparation/input/csv/formatted/AT","--country", "AT"])
Cli().parse(["--insert", "inputs", "--dir", "/home/frox/tmobile/data_mar12/preparation/input/csv/formatted/CZ", "--country", "CZ"])
Cli().parse(["--insert", "inputs", "--dir", "/home/frox/tmobile/data_mar12/preparation/input/csv/formatted/DE", "--country", "DE"])
Cli().parse(["--insert", "inputs", "--dir", "/home/frox/tmobile/data_mar12/preparation/input/csv/formatted/NL", "--country", "NL"])

Cli().parse(["--insert", "forwards", "--dir", "/home/frox/tmobile/data_mar12/preparation/output/AT/csv/formatted", "--country", "AT"])
Cli().parse(["--insert", "forwards", "--dir", "/home/frox/tmobile/data_mar12/preparation/output/CZ/csv/formatted", "--country", "CZ"])
Cli().parse(["--insert", "forwards", "--dir", "/home/frox/tmobile/data_mar12/preparation/output/DE/csv/formatted", "--country", "DE"])
Cli().parse(["--insert", "forwards", "--dir", "/home/frox/tmobile/data_mar12/preparation/output/NL/csv/formatted", "--country", "NL"])
