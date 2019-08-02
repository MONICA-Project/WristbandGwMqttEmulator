import datetime
import signal
import sys
from dictionary_topics import DICTIONARY_OBSERVABLE_TOPICS
from backgroundscheduler import BackgroundSchedulerConfigure
from mqtt_client import MQTTClient
from messagesender import Publisher
from settings import Settings


def periodic_publish():
    try:
        if Settings.list_events_publish:
            return
        Settings.list_events_publish.append(1)
        print('Called periodic publish, time: {}'.format(datetime.datetime.utcnow().isoformat()))
        Publisher.publish_topics(dictionary_observables=DICTIONARY_OBSERVABLE_TOPICS,
                                 hostname=Settings.hostname,
                                 port=Settings.port,
                                 client_id=Settings.client_id)
        Settings.list_events_publish.clear()
    except Exception as ex:
        print('periodic_publish Exception: {}'.format(ex))


def signal_handler(signal, frame):
    """ This signal handler overwrite the default behaviour of SIGKILL (pressing CTRL+C). """

    print('You pressed Ctrl+C!')
    print("\nThe MQTT listener is turning down now...\n")
    BackgroundSchedulerConfigure.stop()
    MQTTClient.disconnect()
    print("\nAPPLICATION STOPPED\n")
    sys.exit(0)


if __name__ == '__main__':
    try:
        print('Started Application MQTT')
        signal.signal(signal.SIGINT, signal_handler)

        BackgroundSchedulerConfigure.configure()
        BackgroundSchedulerConfigure.add_job(func=periodic_publish,
                                             interval_secs=20,
                                             id_job=Settings.job_id)
        BackgroundSchedulerConfigure.start()

        MQTTClient.initialize(client_id=Settings.client_id)
        MQTTClient.connect(hostname=Settings.hostname,
                           port=Settings.port)
    except Exception as ex:
        print('Exception Main: {}'.format(ex))
