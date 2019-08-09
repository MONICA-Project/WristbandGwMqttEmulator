import datetime
import signal
import sys
from backgroundscheduler import BackgroundSchedulerConfigure
from mqtt_client import MQTTClient
from messagesender import Publisher
from settings import Settings
from typing import List, Dict
from utilitytimer import TimerRequest

DEVICES = {}


def main():
    try:
        print('Started Application MQTT')
        signal.signal(signal.SIGINT, signal_handler)

        print('Generating MQTT Devices...')
        global DEVICES
        DEVICES = generate_devices_dictionary()

        print('Started Application MQTT. Number Wristband Emulated: {}'.format(len(DEVICES)))
        BackgroundSchedulerConfigure.configure()
        BackgroundSchedulerConfigure.add_job(func=periodic_publish,
                                             interval_secs=Settings.interval_sending_secs,
                                             id_job=Settings.job_id)
        BackgroundSchedulerConfigure.start()

        TimerRequest.configure_timer(func=terminate_during_execution, timeout=1)

        Publisher.configure(client_id=Settings.client_id, hostname=Settings.hostname, port=Settings.port)
        Publisher.connect()
        Publisher.loop_wait()
    except Exception as ex:
        print('Exception Main: {}'.format(ex))


def generate_devices_dictionary():
    topic = Settings.topic_prefix+"SCRAL/"+Settings.device+"/"+Settings.property

    devices = {}
    for i in range(0, Settings.device_number):
        if i < 10:
            str_i = "0"+str(i)
        else:
            str_i = str(i)

        devices[i] = [topic, Settings.device_name+str_i]
        print(str_i+": "+str(devices[i]))

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
        print('terminate_during_execution Called')
        signal_handler(signal=signal.SIGINT, frame=None)
    except Exception as ex:
        print('terminate_during_execution Exception: {}'.format(ex))


def periodic_publish():
    try:
        if Settings.list_events_publish:
            return
        Settings.list_events_publish.append(1)
        print('Called periodic publish, time: {}'.format(datetime.datetime.utcnow().isoformat()))
        Publisher.publish_topics(dictionary_observables=DEVICES)
        Settings.list_events_publish.clear()

        if Settings.just_one_time_execution == 1:
            print('\nRequest ONE TIME Execution')
            TimerRequest.action_timer()

    except Exception as ex:
        print('periodic_publish Exception: {}'.format(ex))


def signal_handler(signal, frame):
    """ This signal handler overwrite the default behaviour of SIGKILL (pressing CTRL+C). """

    print("\nThe MQTT listener is turning down now...\n")
    TimerRequest.clear_timer()
    BackgroundSchedulerConfigure.stop()
    MQTTClient.disconnect()
    Publisher.stop_client()
    print("\nAPPLICATION STOPPED\n")
    sys.exit(0)


if __name__ == '__main__':
    main()
