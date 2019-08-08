import paho.mqtt.client as mqtt


class MQTTClient:
    client_mqtt = None
    flag_connected = 0
    list_topics = None

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        try:
            if MQTTClient.flag_connected == 1:
                return

            MQTTClient.flag_connected = 1

            print('MQTT on_connect event')

            if not MQTTClient.list_topics:
                print('MQTT Registration to all topics')
                client.subscribe(topic='#', qos=0)
                return

            client.subscribe(MQTTClient.list_topics)
            print('MQTT Registration to specific topics: {}'.format(len(MQTTClient.list_topics)))
        except Exception as ex:
            print('Exception: {}'.format(ex))

    @staticmethod
    def on_disconnect(client, userdata, flags, rc):
        try:
            MQTTClient.flag_connected = 0

            print('Client Disconnected')
            # client.reconnect()
        except Exception as ex:
            print('Exception: {}'.format(ex))

    @staticmethod
    def on_unsubscribe(client, userdata, level, buf):
        print('Unsubscribed Success! {}'.format(buf))

    @staticmethod
    def on_subscribe(client, userdata, level, buf):
        print('Subscribed Success! {}'.format(len(buf)))

    @staticmethod
    def on_message(client, userdata, message):
        try:
            if client:
                return
            print('Message topic: ' + message.topic)
            print('Message received: ' + str(message.payload))
        except Exception as ex:
            print(ex)

    @staticmethod
    def connect(hostname: str, port: int):
        try:
            MQTTClient.client_mqtt.connect(host=hostname, port=port)
            print('MQTT Client Test Connected to host: {0}, port: {1}'.format(hostname, port))
            MQTTClient.client_mqtt.loop_forever()
        except Exception as ex:
            print('MQTT Client connect Exception: {}'.format(ex))

    @staticmethod
    def disconnect():
        try:
            if not MQTTClient.client_mqtt:
                return
            MQTTClient.client_mqtt.disconnect()
            print('MQTT Client Test Disonnected')
            MQTTClient.client_mqtt.loop_stop()
        except Exception as ex:
            print('MQTT Client connect Exception: {}'.format(ex))

    @staticmethod
    def set_list_topics(list_topics: list):
        MQTTClient.list_topics = list_topics

    @staticmethod
    def initialize(client_id: str):
        try:
            MQTTClient.client_mqtt = mqtt.Client(client_id)
            MQTTClient.client_mqtt.on_connect = MQTTClient.on_connect
            MQTTClient.client_mqtt.on_disconnect = MQTTClient.on_disconnect
            MQTTClient.client_mqtt.on_message = MQTTClient.on_message
            MQTTClient.client_mqtt.on_subscribe = MQTTClient.on_subscribe
        except Exception as ex:
            print('MQTT Client initialize Exception: {}'.format(ex))
