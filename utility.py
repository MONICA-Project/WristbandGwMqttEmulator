import logging
import signal
import sys
import os
from typing import Union
from mqtt_client import MQTTClient
from utilitytimer import TimerRequest

from backgroundscheduler import BackgroundSchedulerConfigure
from messagesender import Publisher
from settings import Settings, PermanentSettings
from constants import DEFAULT_LOG_FORMATTER, DEBUG_KEY


def initialize_log():
    if not PermanentSettings.containerized:
        init_log_debug_mode(Settings.debug)
    else:
        try:
            debug = bool(os.environ[DEBUG_KEY])
            init_log_debug_mode(debug)
        except KeyError as ke:
            print("Missing debug environmental variable")
            init_log_debug_mode(False)


def init_log_debug_mode(debug: bool):
    if debug:
        configure_log(logging.DEBUG)
    else:
        configure_log(logging.INFO)
    logging.info("Debug mode: " + str(debug))


def configure_log(debug_level: Union[int, str]):
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


def terminate_during_execution():
    try:
        logging.info('terminate_during_execution called')
        signal_handler(signal=signal.SIGINT, frame=None)
    except Exception as ex:
        logging.error('terminate_during_execution exception: {}'.format(ex))