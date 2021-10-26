
# Assignment

This repository is dedicated to build a Message Broker Service using Apache Kafka and Google Pub/Sub for Image Recognition Model.

## Table of Contents
- Installation
- Requirements
- Usage
- Development
- License

## Installation
[(Back to Top)](#table-of-contents)

To use this project, first clone the repo using the following command:

```git init```

```git clone https://github.com/LaxmanSinghTomar/assignment.git```


## Requirements
[(Back to Top)](#table-of-contents)

- In order to use the Kafka, you are required to setup and start Apache Kafka Zookeeper and Kafka Server.
- In order to use the Google Pub/Sub Modules, you will require Google Application Credentials. Try to follow [this](https://cloud.google.com/pubsub/docs/quickstart-client-libraries). 

## Usage

[(Back to Top)](#table-of-contents)

Install the required libraries & packages using:

```sh
pip install requirements.txt
```

To train the model use, the following command:

```sh
python3 src/models/train.py
```

To run the application use:

```sh
python3 src/app.py
```

## Development
[(Back to Top)](#table-of-contents)
<pre>
├── models                      # Model Directory comprising Trained Model Files
│   └── fashion_mnist_cnn
│       ├── assets
│       ├── keras_metadata.pb
│       ├── saved_model.pb
│       └── variables
│           ├── variables.data-00000-of-00001
│           └── variables.index
├── notebooks               # Jupyter Notebook comprising Model Experimentation.
│   └── train_CNN.ipynb
└── src                     # Python Scripts
    ├── aerospike                           # AeroSpike DB
    │   └──aerospike_config.properties
    ├── app.py                              # Main Application
    ├── config                              # Configuration Directory
    │   ├── app_config.properties
    │   ├── constants_config.py
    │   ├── logging_config.py
    │   └── runtime_config.py
    ├── kafka_module                        # Kafka Module Scripts + Configs
    │   ├── consumer_config.properties
    │   ├── consumer.py
    │   ├── producer_config.properties
    │   └── producer.py
    ├── logs                                # Generated Logs
    │   ├── logs__main__.logs
    │   └── logs__main__.logs.2021-10-25
    ├── models                              # Model Training & Utilities
    │   ├── train.py
    │   └── utils.py
    └── pubsub                              # Pub/Sub Module Scripts + Configs
        ├── publisher_config.properties
        ├── publisher.py
        ├── subscriber_config.properties
        └── subscriber.py
</pre>


## License
[(Back to top)](#table-of-contents)

[GNU General Public License version 3](https://opensource.org/licenses/GPL-3.0)
