# Kafka Producer

# Importing Libraries
from kafka import KafkaProducer

class Producer():
    def __init__(self, config, logger):
        self.kafkaConfig = config
        self.logger = logger
        self.producer = self.create_producer()

    def create_producer(self):
        return KafkaProducer(**self.kafkaConfig)

    def push_records(self, requestID, labelNames):
        if len(requestID) == 0:
            return False
        try:
            for requestID, classLabel in zip(requestID, labelNames):
                self.producer.send('test-topic-send', {requestID: classLabel})
            self.logger.info(f"Successfully Pushed Records!")
            return True
        except Exception as e:
            self.logger.error(f"Failed to push Records!{e}")
            return False

        