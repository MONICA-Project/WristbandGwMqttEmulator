import datetime
import os
import signal
import numpy as np
import logging

from backgroundscheduler import BackgroundSchedulerConfigure
from messagesender import Publisher
from settings import Settings, PermanentSettings
from utilitytimer import TimerRequest

import constants
import utility

DEVICES = {}


def main():
    np.random.seed(0)
    signal.signal(signal.SIGINT, utility.signal_handler)
    utility.initialize_log()

    if not PermanentSettings.containerized:
        logging.info("***Application mode*** variables taken form Setting class.")
        interval_secs = Settings.interval_sending_secs
        mqtt_hostname = Settings.hostname
        mqtt_port = Settings.port
    else:
        logging.info("***Containerized mode*** variables taken from environmental variables.")
        try:
            interval_secs = int(os.environ[constants.BURST_INTERVAL_KEY])
            mqtt_hostname = os.environ[constants.MQTT_HOSTNAME_KEY]
            mqtt_port = int(os.environ[constants.MQTT_PORT_KEY])
        except KeyError as ke:
            logging.critical("Environmental variable not found: "+str(ke))
            exit(1)
    try:
        logging.info('Generating MQTT Devices...')
        global DEVICES
        DEVICES = generate_devices_dictionary()
        logging.info('Total number of wristband emulated: {}'.format(len(DEVICES)))

        BackgroundSchedulerConfigure.configure()
        BackgroundSchedulerConfigure.add_job(func=periodic_publish, interval_secs=interval_secs,
                                             id_job=PermanentSettings.job_id)
        BackgroundSchedulerConfigure.start()
        TimerRequest.configure_timer(func=utility.terminate_during_execution, timeout=1)
        logging.debug('Periodic burst configured and scheduler started!')

        client_id = PermanentSettings.client_id
        logging.info('Connecting to "'+mqtt_hostname+':'+str(mqtt_port)+'" with id: "'+client_id+'"')
        Publisher.configure(client_id=client_id, hostname=mqtt_hostname, port=mqtt_port)
        Publisher.connect()
        Publisher.loop_wait()

    except Exception as ex:
        logging.critical('Exception Main: {}'.format(ex))


def generate_devices_dictionary():
    if not PermanentSettings.containerized:
        topic_prefix = Settings.topic_prefix
        device_number = Settings.device_number
    else:
        try:
            topic_prefix = os.environ[constants.GOST_TOPIC_PREFIX]
            device_number = int(os.environ[constants.DEVICE_NUMBER_KEY])
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


if __name__ == '__main__':
    main()
