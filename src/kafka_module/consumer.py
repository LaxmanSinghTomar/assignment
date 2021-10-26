# Kafka Consumer

# Importing Libraries
from kafka import KafkaConsumer

class Consumer():
    def __init__(self, topics, logger, config):
        self.kafkaTopics = topics
        self.kafkaConfig = topics
        self.logger = logger
        self.consumer = self.create_consumer()

    def create_consumer(self):
        return KafkaConsumer(self.kafkaTopics, self.kafkaConfig)

    def fetch_records(self, bufferSize):
        consumedMessage, fetched = [], 0
        for message in self.consumer:
            try:
                consumedMessage.append(message.value.decode("utf-8"))
                fetched+=1
                if fetched > bufferSize:
                    break
            except Exception as e:
                self.logger.warning(f"Failed to consumer messages{e}!")

        return consumedMessage       

