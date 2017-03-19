class IntegrationConfig:
  @staticmethod
  def kafkaServers():
    return "127.0.0.2:9092"

  @staticmethod
  def getEmailConfig():
    emailConfig = {}
    emailConfig['to'] = "mediation-monitoring@seznam.cz"
    emailConfig['from'] = "mediation-monitoring@seznam.cz"
    emailConfig['login'] = "mediation-monitoring@seznam.cz"
    emailConfig['password'] = "mediation1."
    emailConfig['smtpHostname'] = "smtp.seznam.cz"
    return emailConfig
