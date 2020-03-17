# Wristband Gateway MQTT Emulator

This repository contains an application that emulates the behaviour of the Wristband Gateway (GW) that has been used in the MONICA project.
Differently from the first version of the Wristband GW
(which uses [REST protocol](https://en.wikipedia.org/wiki/Representational_state_transfer)),
this application has been configured to send wristband messages to the IoT platform by using the [MQTT protocol](http://mqtt.org/). 

The application generates wristband positions according to a 2-D Gaussian distribution centered in a specific position, provided as input and expressed in terms of latitude and longitude, and a 2-D covariance matrix, whose main parameters can be provided as input too.

This application has been developed by Luca Mannella starting from the 
_SCRAL emulator_ developed by Antonio Defina with contributions from Francesco Sottile (all from LINKS Foundation).

## Getting Started
To test the application using the source code you should follow this section, otherwise if you want to work with Docker
container follow the "Docker section" under the "Deployment" section.

### Starting an MQTT broker or the MONICA Environment
To make the application work properly, it is necessary to have AT LEAST an
[MQTT broker](https://www.hivemq.com/blog/mqtt-essentials-part-3-client-broker-connection-establishment/).
You can use whatever [broker](https://github.com/mqtt/mqtt.github.io/wiki/brokers) you want, but we have tested
 our solution only with [Eclipse Mosquitto](https://mosquitto.org/).

If you need just an MQTT broker, you can start an "Eclipse Mosquitto" broker going inside "docker-compose" folder
and running the following command:
```bash
$ docker-compose -f docker-compose-broker.yml up
```

If you want to test the Wristband GW emulator in the "edge layer" of the MONICA IoT ecosystem,
you can go inside the "docker-compose" folder and enter the following command:
```bash
$ docker-compose -f docker-compose.yml up
```
This compose file will start an Eclipse Mosquitto Broker, the storage backend of MONICA ecosystem (a GOST server)
and the _Wristband MQTT module_ of the Smart City Adaptation Layer (SCRAL).

Once you have created the MONICA environment, you can check if data are correctly flowing by looking at the
"local" SCRAL REST page at this url: http://localhost:8000/scral/v1.0/wristband-gw,
the GOST dashboard at: http://localhost:8080 or the GOST main entrypoint at: http://localhost:8080/v1.0

To have more information about these applications, please visit the official github pages of
[GOST](https://github.com/gost/server) and [SCRAL framework](https://github.com/MONICA-Project/WristbandGwMqttEmulator)
or the official [MONICA developer website](https://monica-project.github.io/).

Note: you can add "-d" in the end of the command if you want to detach the containers and don't see their output on
your console.

### Configure and run the Python application 
To properly configure the application, you should go inside the "settings.py" file and modify some values contained
inside the "Setting" and "PermanentSettings" classes.

The value contained inside "Settings" class are more related to a single execution and can be replaced
with enviromental variables (see Docker section), meanwhile the "PermanentSettings" can be configured
only inside the source code.

**Note**: To use the values contained in the "Setting" class it is important to set the value of "PermanentSettings.containerized"
to False.
```Python
class PermanentSettings:
    containerized = False
    [...]
```
Otherwise, several environmental variables can be used for the configuration of the application (see Docker section).

If the "containerized" value is set to False, and you have at least an MQTT broker already configured,
you can move inside the project main folder and start the Wristband GW emulator simply run the following command
on your console:
```bash 
$ python appmanager.py
```

Note: the wristbands should be previously registered to the SCRAL module through a POST request.
However, in order to simplify the execution, _SCRAL MQTT Wristband module_ is able to automatically
register new wristbands as soon as it receives the first message from a new device not yet registered.

## Deployment
In this section will be explained how to start the dockerized version of this application.

### Docker
To run the latest version of the WristbandGwMqttEmulator, you can run the following commands
(it is necessary to set before the appropriate environmental variables):
```bash
docker run monicaproject/wb_mqtt_emulator:latest
```

To test the whole environment, it is suggested to start the "docker-compose-testing.yml" file with following command:
```bash
$ docker-compose -f docker-compose-testing.yml up
```

Inside the docker-compose file you can find all the variables that are set to a default value.
If you are not familiar about the variables meaning, please use simply the default values.

#### Variables
- MQTT_HOSTNAME: the url of the MQTT broker or the name of the dockerized MQTT container;
- MQTT_PORT: the port on which the MQTT broker is listening;
- DEVICE_NUMBER: total number of emulated wristbands;
- BURST_INTERVAL_SEC: update period of the wristbands, that si the interval of time between two observations send by the same wristband;
- GOST_MQTT_PREFIX: the MQTT topic used by GOST (default value is "GOST/");
- DEBUG: specify if you want more debug logging information (default value is false).

The application is configured to have at most 4 different positions or epicenters, called also stages, around which the positions of wristbands are gererated accorging to a 2-D Gaussian distribution.
If you want to use less stage you  just have to put 0 in the field "DISTR_STAGE_N". 
- STAGE_NAME_1: the name associated to the first epicenter/stage;
- DISTR_STAGE_1: the probability of having a wristband associated to this stage;
- LAT_STAGE_1: the latitude of the first epicenter/stage;
- LON_STAGE_1: the longitude of the first epicenter/stage;
- SIGMA_N_S_1: it is the variance along North-South of the Gaussian distribution (default value 400);
- SIGMA_E_O_1: it is the variance along East-West of the Gaussian distribution (default value 400).

## Development
<!-- Developer instructions. -->

### Prerequisite
This projects depends on Python 3, installation instructions are available [here](https://www.python.org/downloads/).
Furthermore, the library used are the following:
- numpy
- paho-mqtt
- pytz
- apscheduler
- pymap3d

You can download them using:
```bash
pip install <library_name>
```

## Contributing
Contributions are welcome.

Please fork, make your changes, and submit a pull request. For major changes, please open an issue first and discuss it with the other authors.

## Affiliation
![MONICA-Logo](images/monica.png)  
This work is supported by the European Commission through the [MONICA H2020 PROJECT](https://www.monica-project.eu) under grant agreement No 732350.

![SCRAL-Logo](images/SCRAL-Logo-V1.1-reduced.png)<br>
This emulator was designed to interact with the Smart City Resource Adaptation Layer (SCRAL) developed for MONICA project. 
