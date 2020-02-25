import paho.mqtt.client as mqtt
import json
from typing import Dict, Any
import datetime
import logging


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat() + 'Z'

        return json.JSONEncoder.default(self, o)


class ServerMQTT(object):
    client_mqtt = None
    flag_connected = 0
    counter_message_published = 0
    debug_numbernotification = 1
    hostname = str('')
    port = 0
    reference_datetime = None

    @staticmethod
    def get_client_mqtt() -> mqtt.Client:
        return ServerMQTT.client_mqtt

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        try:
            if ServerMQTT.flag_connected == 1:
                return

            ServerMQTT.flag_connected = 1

            logging.info('ServerMQTT on_connect event')
        except Exception as ex:
            logging.critical('Exception: {}'.format(ex))

    @staticmethod
    def on_disconnect(client, userdata, flags, rc):
        try:
            ServerMQTT.flag_connected = 0

            logging.info('ServerMQTT Disconnected')
            client.reconnect()
        except Exception as ex:
            logging.error('ServerMQTT on_disconnect Exception: {}'.format(ex))

    @staticmethod
    def on_publish(client, userdata, result):
        ServerMQTT.counter_message_published += 1

        if (ServerMQTT.counter_message_published % ServerMQTT.debug_numbernotification) == 0:
            interval_secs = (datetime.datetime.utcnow()-ServerMQTT.reference_datetime).total_seconds()
            logging.info('ServerMQTT OnPublish Method raised: {0} RelativeTime: {1}'.format(
                ServerMQTT.counter_message_published, interval_secs))

    @staticmethod
    def configure_client(client_id: str, hostname: str, port: int):
        try:
            ServerMQTT.client_mqtt = mqtt.Client(client_id=client_id, clean_session=True)
            ServerMQTT.client_mqtt.on_connect = ServerMQTT.on_connect
            ServerMQTT.client_mqtt.on_disconnect = ServerMQTT.on_disconnect
            ServerMQTT.client_mqtt.on_publish = ServerMQTT.on_publish
            ServerMQTT.hostname = hostname
            ServerMQTT.port = port
        except Exception as ex:
            logging.critical('ServerMQTT configure_client Exception: {}'.format(ex))

    @staticmethod
    def stop_client():
        try:
            ServerMQTT.get_client_mqtt().disconnect()
            ServerMQTT.get_client_mqtt().loop_stop()
        except Exception as ex:
            logging.error('ServerMQTT stop_client Exception: {}'.format(ex))

    @staticmethod
    def connect_client():
        try:
            ServerMQTT.client_mqtt.connect(host=ServerMQTT.hostname, port=ServerMQTT.port)
            logging.info('ServerMQTT configure_client hostname: {0}, port: {1}'.format(ServerMQTT.hostname, ServerMQTT.port))
            ServerMQTT.reference_datetime = datetime.datetime.utcnow()
        except Exception as ex:
            logging.critical('ServerMQTT configure_client Exception: {}'.format(ex))

    @staticmethod
    def loop_wait():
        try:
            logging.info('ServerMQTT Loop Forever')
            ServerMQTT.get_client_mqtt().loop_forever()
        except Exception as ex:
            logging.critical('ServerMQTT Loop Forever Exception: {}'.format(ex))

    @staticmethod
    def publish(topic: str, dictionary: Dict[str, Any]) -> bool:
        try:
            if ServerMQTT.flag_connected == 0 or not ServerMQTT.client_mqtt:
                return False

            if not dictionary:
                logging.info('No Data To Transfer')
                return False

            string_json = json.dumps(obj=dictionary,
                                     cls=DateTimeEncoder)

            return_info = ServerMQTT.get_client_mqtt().publish(topic=topic, payload=string_json, qos=0, retain=False)

            if not return_info:
                return False

            if return_info.rc != mqtt.MQTT_ERR_SUCCESS:
                logging.error('ServerMQTT Publish Error: {}'.format(str(return_info.rc)))
                return False

            return True

        except Exception as ex:
            logging.error('Exception ServerMQTT PublishBis: {}'.format(ex))
            return False
