import datetime
import smtplib
from email.mime.text import MIMEText

import util
from config import AppConfig

MIN_DELAY = datetime.timedelta(minutes=5)


class EmailSender:
  _instance = None

  def __init__(self):
    super().__init__()
    self.lastComponentEmailTime = {}

  def canSendEmail(self, component):
    lastTime = self.lastComponentEmailTime.get(component, None)
    if lastTime is None:
      return True
    return AppConfig.getCurrentTime() - lastTime > MIN_DELAY

  def sendEmail(self, component, body):
    if not self.canSendEmail(component):
      return
    msg = MIMEText(body +
                   "\ntime:" + util.dateToTimeString(AppConfig.getCurrentTime()) +
                   "\ncomponent:" + component
                   )
    msg['Subject'] = 'Mediation monitoring: ' + component
    msg['From'] = "mediation-monitoring@seznam.cz"
    msg['To'] = "mediation-monitoring@seznam.cz"

    s = smtplib.SMTP('smtp.seznam.cz')
    s.login('mediation-monitoring@seznam.cz', 'mediation1.')
    s.send_message(msg)
    self.lastComponentEmailTime[component] = AppConfig.getCurrentTime()
    s.quit()

  @staticmethod
  def instance():
    if EmailSender._instance is None:
      EmailSender._instance = EmailSender()
    return EmailSender._instance
