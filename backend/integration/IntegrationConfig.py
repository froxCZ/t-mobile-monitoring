from common import AppConfig


class IntegrationConfig:
  @staticmethod
  def kafkaServers():
    return AppConfig.getIntegrationConfig().get("kafka", {}).get("servers", None)

  @staticmethod
  def outputTopic():
    return AppConfig.getIntegrationConfig().get("kafka", {}).get("outputTopic", None)

  @staticmethod
  def inputTopic():
    return AppConfig.getIntegrationConfig().get("kafka", {}).get("inputTopic", None)

  @staticmethod
  def getEmailConfig():
    return AppConfig.getIntegrationConfig().get("email",None)
