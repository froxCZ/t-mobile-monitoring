import datetime
import smtplib
from email.mime.text import MIMEText

from common import AppConfig
from common import util
from integration import IntegrationConfig

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
    emailConfig = IntegrationConfig.getEmailConfig()
    if emailConfig is None:
      return
    if not self.canSendEmail(component):
      return
    msg = MIMEText(body +
                   "\ntime:" + util.dateToTimeString(AppConfig.getCurrentTime()) +
                   "\ncomponent:" + component
                   )

    msg['Subject'] = 'Mediation monitoring: ' + component
    msg['From'] = emailConfig["from"]
    msg['To'] = emailConfig["to"]

    s = smtplib.SMTP(emailConfig["smtpHostname"])
    s.login(emailConfig["login"], emailConfig["password"])
    s.send_message(msg)
    self.lastComponentEmailTime[component] = AppConfig.getCurrentTime()
    s.quit()

  @staticmethod
  def instance():
    if EmailSender._instance is None:
      EmailSender._instance = EmailSender()
    return EmailSender._instance
