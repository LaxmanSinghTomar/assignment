# Importing Libraries

from logging import Logger
from sys import meta_path
from google.cloud import pubsub_v1
from google.api_core import retry



class Subscriber():
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.subscriber, self.topic_path = self.create_subscriber()

    def create_subscriber(self):
        subscriber = pubsub_v1.SubscriberClient()
        topic_path = subscriber.topic_path(self.config['project'], self.config['topic'])
        return subscriber, topic_path

    def fetch_records(self):
        with self.subscriber:
            response = self.subscriber.pull(
                request = {'subscription': self.config['subscription_path'],
                            'max_messages': self.config['max_messages']},
                            retry = retry.Retry(deadline=300),)
           
            consumedMessage, fetched = [], 0
            for msg in response.received_messages:
                consumedMessage.append(msg.message.data)
        return consumedMessage

