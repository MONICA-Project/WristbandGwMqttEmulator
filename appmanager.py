import datetime
import os
import signal
import sys
import numpy as np

from backgroundscheduler import BackgroundSchedulerConfigure
from mqtt_client import MQTTClient
from messagesender import Publisher
from settings import Settings, PermanentSettings
from typing import Union
from utilitytimer import TimerRequest
import logging
import constants

DEVICES = {}
DEFAULT_LOG_FORMATTER = "%(asctime)s.%(msecs)04d %(name)-7s %(levelname)s: %(message)s"
DEBUG = True


def main():
    np.random.seed(0)
    init_logger(logging.DEBUG)

    if DEBUG:
        interval_secs = Settings.interval_sending_secs
        mqtt_hostname = Settings.hostname
        mqtt_port = Settings.port
    else:
        try:
            interval_secs = int(os.environ[constants.BURST_INTERVAL_KEY])
            mqtt_hostname = os.environ[constants.MQTT_HOSTNAME_KEY]
            mqtt_port = int(os.environ[constants.MQTT_PORT_KEY])
        except KeyError as ke:
            logging.critical("Environmental variable not found: "+str(ke))
            exit(1)
    try:
        logging.info('Started Application MQTT')
        signal.signal(signal.SIGINT, signal_handler)

        logging.info('Generating MQTT Devices...')
        global DEVICES
        DEVICES = generate_devices_dictionary()

        logging.info('Started Application MQTT. Number Wristband Emulated: {}'.format(len(DEVICES)))
        BackgroundSchedulerConfigure.configure()
        BackgroundSchedulerConfigure.add_job(func=periodic_publish, interval_secs=interval_secs,
                                             id_job=PermanentSettings.job_id)
        BackgroundSchedulerConfigure.start()
        TimerRequest.configure_timer(func=terminate_during_execution, timeout=1)

        client_id = PermanentSettings.client_id
        logging.info("Connecting to "+mqtt_hostname+":"+str(mqtt_port)+" with id: "+client_id)
        Publisher.configure(client_id=client_id, hostname=mqtt_hostname, port=mqtt_port)
        Publisher.connect()
        Publisher.loop_wait()

    except Exception as ex:
        logging.critical('Exception Main: {}'.format(ex))


def generate_devices_dictionary():
    if DEBUG:
        topic_prefix = Settings.topic_prefix
        device_number = Settings.device_number
    else:
        try:
            topic_prefix = os.environ[constants.GOST_TOPIC_PREFIX]
            device_number = int(os.environ[constants.DEVICE_NUMBER])
        except KeyError as ke:
            logging.critical("Environmental variable not found: "+str(ke))
            exit(1)

    devices = {}
    topic = topic_prefix + constants.MQTT_SCRAL_PREFIX + PermanentSettings.device + "/" + PermanentSettings.property
    for i in range(0, device_number):
        if i < 10:
            str_i = "0"+str(i)
        else:
            str_i = str(i)

        devices[i] = [topic, PermanentSettings.device_name+str_i]
        logging.debug(str_i+": "+str(devices[i]))

    return devices


def terminate_during_execution():
    try:
        logging.info('terminate_during_execution called')
        signal_handler(signal=signal.SIGINT, frame=None)
    except Exception as ex:
        logging.error('terminate_during_execution exception: {}'.format(ex))


def periodic_publish():
    try:
        if PermanentSettings.list_events_publish:
            return
        PermanentSettings.list_events_publish.append(1)
        logging.info('Called periodic publish, time: {}'.format(datetime.datetime.utcnow().isoformat()))
        Publisher.publish_topics(dictionary_observables=DEVICES)
        PermanentSettings.list_events_publish.clear()

        if PermanentSettings.just_one_time_execution == 1:
            logging.info('\nRequest ONE TIME Execution')
            TimerRequest.action_timer()

    except Exception as ex:
        logging.error('periodic_publish Exception: {}'.format(ex))


def init_logger(debug_level: Union[int, str]):
    """ This function configure the logger according to the specified debug_level taken from logging class. """

    logging.basicConfig(format="%(message)s")
    logging.getLogger().setLevel(level=debug_level)
    logging.getLogger().handlers[0].setFormatter(logging.Formatter(DEFAULT_LOG_FORMATTER, datefmt="(%b-%d) %H:%M:%S"))


def signal_handler(signal, frame):
    """ This signal handler overwrite the default behaviour of SIGKILL (pressing CTRL+C). """

    logging.info("\nThe MQTT listener is turning down now...\n")
    TimerRequest.clear_timer()
    BackgroundSchedulerConfigure.stop()
    MQTTClient.disconnect()
    Publisher.stop_client()
    logging.info("\nAPPLICATION STOPPED\n")
    sys.exit(0)


if __name__ == '__main__':
    main()
