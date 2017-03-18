import json
import threading

from kafka import KafkaConsumer

from config import AppConfig


class MediationDataConsumer(threading.Thread):
  daemon = False

  def run(self):
    consumer = KafkaConsumer(bootstrap_servers=AppConfig.kafkaServers(),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id="demonstration")
    consumer.subscribe(['mediationMonitoringStatus'])

    for message in consumer:
      print(json.loads(message.value.decode('utf-8')))


def main():
  threads = [
    MediationDataConsumer()
  ]

  for t in threads:
    t.start()


if __name__ == "__main__":
  main()
