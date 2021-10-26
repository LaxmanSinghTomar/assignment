# Kafka Consumer

# Importing Libraries
from logging import Logger
from google.cloud import pubsub_v1
from json import dumps

class Publisher():
    def __init__(self, logger, config):
        self.logger = logger 
        self.config = config
        self.publisher, self.topic_path = self.create_publisher()

    def create_publisher(self):
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(**self.config)
        return publisher, topic_path

    def push_records(self, requestID, labelNames):
        if len(requestID) == 0:
            return False
        try:
            for requestID, classLabel in zip(requestID, labelNames):
                data = dumps({requestID: classLabel})
                message_publish_status = self.publisher.publish(self.topic_path, data)
                self.logger.info(f"Pushed Record {message_publish_status}")
            self.logger.info("Successfully Pushed Records...")
            return True
        except Exception as e:
            self.logger.error(f"Failed to push records{e}")
            return False
        