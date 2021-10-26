# Application

# Importing Libraries
from pubsub.publisher import Publisher
from pubsub.subscriber import Subscriber
from kafka_module.producer import Producer
from kafka_module.consumer import Consumer
from models.utils import Utils
from config.logging_config import get_logger
from config import runtime_config
from config.constants_config import model_path
from json import loads, dumps
from datetime import datetime
import numpy as np
import aerospike
import sys
sys.path.insert(1, "src/")


def connect_aerospike(host, port, namespace = None):
    """
    Setup the connectiion to the AeroSpike Client.

    Args:
        host: Array of Host IPs
        port: Port Number of each host

    Returns:
        Connected Aerospike Client
    """
    try:
        hosts = host.split(",")
        aerospike_config_dict = {'hosts': list(tuple([host, int(port)]) for host in hosts)}
        aerospike_client = aerospike.client(aerospike_config_dict).connect()
        return aerospike_client
    except:
        return None

def push_records(aerospikeClient, requestID, labelNames, namespace, logger):
    """
    Push Records to Kafka Producer & Aerospike Database.

    Args:
        aerospikeClient: AeroSpike Client.
        requestID: Request ID of Messages.
        labelNames: Prediction Class Labels.
        namespace: Name of the Database.
    """
    logger.info(f"Pushing Records to NoSQL Database...")
    try:
        for requestID, classLabel in zip(requestID, labelNames):
            key = (namespace, 'test-table-name', str(requestID))
            if aerospikeClient is not None or aerospikeClient.closed() is not True:
                aerospikeClient.put(key, classLabel)
            logger.info(f"Successfully Pushed Records...")
            return True
    except Exception as e:
        logger.error(f"Failed to Push Records {e}")
        return False


if __name__ == "__main__":
    logger = get_logger(logger_name = __name__)
    logger.info("Application Initialized...")
    logger.info("Loading Configuration Files")

    appConfig = runtime_config.getAppConfig()
    aerospikeConfig = runtime_config.getAeroSpikeConfig()
    kafkaConfig = runtime_config.getKafkaConfig()
    pubSubConfig = runtime_config.getPubSubConfig()

    consumerConfig = kafkaConfig['kafka_consumer_config']
    producerConfig = kafkaConfig['kafka_producer_config']
    subscriberConfig = pubSubConfig['pub_sub_subscriber_config']
    publisherConfig = pubSubConfig['pub_sub_publisher_config']

    logger.info("Creating Kafka Producer & Consumer Clients")
    consumerModule = Consumer(topics = "test-topics", config = consumerConfig, logger = logger)
    producerModule = Producer(producerConfig, logger = logger)

    logger.info("Creating Google Pub/Sub Clients")
    pubisherModule = Publisher(config = publisherConfig, logger = logger)
    subscriberModule = Subscriber(config = subscriberConfig, logger = logger)

    logger.info("Fetching Model Utilities")
    modelUtilsModule = Utils(model_path = model_path, logger = logger)

    logger.info("Creating Aerospike Client")
    aerospikeClient = connect_aerospike(aerospikeConfig['host'], aerospikeConfig['port'], aerospikeConfig['namespace'])

    usePubSub = appConfig['usePubSub']
    bufferSize = appConfig['client.buffer.size']
    logger.info(f"Using PubSub {usePubSub}")


    while True:
        if usePubSub == True:
            """
            Fetch Records using Subscriber, use Model for Inference and
            push to Publisher & Aerospike DB.
            """
            consumedMessage = subscriberModule.fetch_records(bufferSize = bufferSize)
            requestID, classLabels = modelUtilsModule.inference(consumedMessage=consumedMessage)
            pushOut = pubisherModule.push_records(requestID=requestID, labelNames=classLabels)

        else:
            """
            Fetch Records using Kafka Consumer, use Model for Inference and
            push to Producer & Aerospike DB.
            """
            consumedMessage = consumerModule.fetch_records(bufferSize=bufferSize)
            requestID, classLabels = modelUtilsModule.inference(consumedMessage=consumedMessage)
            pushOut = producerModule.push_records(requestID=requestID, labelNames=classLabels)

        pushAeroSpike = push_records(aerospikeClient, requestID = requestID, labelNames=classLabels, namespace=aerospikeConfig['namespace'], logger=logger)
        logger.info(f"Producer Records Push Status {pushOut}, Aerospike Records Push Status {pushAeroSpike}")
