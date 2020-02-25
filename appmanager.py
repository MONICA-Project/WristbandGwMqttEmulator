import datetime
import signal
import sys
import numpy as np

from backgroundscheduler import BackgroundSchedulerConfigure
from mqtt_client import MQTTClient
from messagesender import Publisher
from settings import Settings, PermanentSettings
from typing import List, Dict, Union
from utilitytimer import TimerRequest
import logging

DEVICES = {}
DEFAULT_LOG_FORMATTER = "%(asctime)s.%(msecs)04d %(name)-7s %(levelname)s: %(message)s"


def main():
    try:
        np.random.seed(0)
        init_logger(logging.DEBUG)

        logging.info('Started Application MQTT')
        signal.signal(signal.SIGINT, signal_handler)

        logging.info('Generating MQTT Devices...')
        global DEVICES
        DEVICES = generate_devices_dictionary()

        logging.info('Started Application MQTT. Number Wristband Emulated: {}'.format(len(DEVICES)))
        BackgroundSchedulerConfigure.configure()
        BackgroundSchedulerConfigure.add_job(func=periodic_publish,
                                             interval_secs=Settings.interval_sending_secs,
                                             id_job=PermanentSettings.job_id)
        BackgroundSchedulerConfigure.start()

        TimerRequest.configure_timer(func=terminate_during_execution, timeout=1)

        Publisher.configure(client_id=PermanentSettings.client_id, hostname=Settings.hostname, port=Settings.port)
        Publisher.connect()
        Publisher.loop_wait()
    except Exception as ex:
        logging.critical('Exception Main: {}'.format(ex))


def generate_devices_dictionary():
    topic = Settings.topic_prefix+"SCRAL/"+PermanentSettings.device+"/"+PermanentSettings.property

    devices = {}
    for i in range(0, Settings.device_number):
        if i < 10:
            str_i = "0"+str(i)
        else:
            str_i = str(i)

        devices[i] = [topic, PermanentSettings.device_name+str_i]
        logging.debug(str_i+": "+str(devices[i]))

    return devices


def extract_list_topics(dictionary_obs: Dict[int, List[str]]) -> list:
    if not dictionary_obs:
        return None

    list_topics = list()

    for key in dictionary_obs:
        if dictionary_obs[key] is None:
            continue
        list_elements = dictionary_obs[key]
        topic = list_elements[0]
        record_topic = (topic, 0)

        list_topics.append(record_topic)

    return list_topics


def terminate_during_execution():
    try:
        logging.info('terminate_during_execution Called')
        signal_handler(signal=signal.SIGINT, frame=None)
    except Exception as ex:
        logging.error('terminate_during_execution Exception: {}'.format(ex))


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
