# Configurations Fetcher

# Importing Libraries
from jproperties import Properties
from config.constants_config import *
import pathlib
import os
import sys
sys.path.insert(1, "src/config/")


# Defining Parent Path
path = pathlib.Path(__file__).resolve().parent.parent
print(path)


def getKafkaConfig():
    """
    Load Configuration for Kafka Producer & Consumer from respective Config Files.

    Returns:
        Kafka Producer Configuration, Kafka Consumer Configuration.
    """
    kafka_consumer_config = Properties()
    with open(os.path.join(path, str(consumer_config_path)), "rb") as f:
        kafka_consumer_config.load(f, "utf-8")

    kafka_producer_config = Properties()
    with open(os.path.join(path, str(producer_config_path)), "rb") as f:
        kafka_producer_config.load(f, "utf-8")

    return {'kafka_consumer_config': kafka_consumer_config,
            'kafka_producer_config': kafka_producer_config}


def getPubSubConfig():
    """
    Load Configuration for Google Publisher & Subscriber from respective Config Files.

    Returns:
        Google Publisher Configuration, Kafka Subscriber Configuration.
    """
    pub_sub_subscriber_config = Properties()
    with open(os.path.join(path, str(subscriber_config_path)), "rb") as f:
        pub_sub_subscriber_config.load(f, "utf-8")

    pub_sub_publisher_config = Properties()
    with open(os.path.join(path, str(publisher_config_path)), "rb") as f:
        pub_sub_publisher_config.load(f, "utf-8")

    return {'pub_sub_subscriber_config': pub_sub_subscriber_config,
            'pub_sub_publisher_config': pub_sub_publisher_config}


def getAeroSpikeConfig():
    """
    Load Configuration for Aerospike from respective Config Files.

    Returns:
        Aerospike Configuration.
    """
    aerospike_config = Properties()
    with open(os.path.join(path, str(aerospike_config_path)), "rb") as f:
        aerospike_config.load(f, "utf-8")
    return aerospike_config


def getAppConfig():
    """
    Load Configuration for Application.

    Returns:
        Application Configuration.
    """
    app_config = Properties()
    with open(os.path.join(path, str(app_config_path)), "rb") as f:
        app_config.load(f, "utf-8")
    return app_config
