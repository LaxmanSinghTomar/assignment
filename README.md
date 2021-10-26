
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

## License
[(Back to top)](#table-of-contents)

[GNU General Public License version 3](https://opensource.org/licenses/GPL-3.0)