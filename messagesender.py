from observables import Localization
from mqtt_publisher import ServerMQTT


class Publisher(object):
    @staticmethod
    def configure(client_id: str, hostname: str, port: int):
        ServerMQTT.configure_client(client_id=client_id, hostname=hostname, port=port)

    @staticmethod
    def connect():
        ServerMQTT.connect_client()

    @staticmethod
    def loop_wait():
        ServerMQTT.loop_wait()

    @staticmethod
    def stop_client():
        ServerMQTT.stop_client()

    @staticmethod
    def publish_topics(dictionary_observables: dict):
        try:
            if not dictionary_observables:
                return

            counter_message_sent = 0

            for iot_id in dictionary_observables:
                list_topic_tagid = dictionary_observables[iot_id]

                if len(list_topic_tagid) < 2:
                    continue

                topic = list_topic_tagid[0]
                tagId = list_topic_tagid[1]

                localization = Localization(tag_id=tagId,
                                            iot_id=iot_id,
                                            lat=55.67298336627162,
                                            lon=12.56703788516)
                ServerMQTT.publish(topic=topic,
                                   dictionary=localization.to_dictionary())

                counter_message_sent += 1

                if (counter_message_sent % 125) == 0:
                    print('MQTT Publish Messages: {}'.format(counter_message_sent))

            print('MQTT Publish Messages Completed: {}'.format(counter_message_sent))
        except Exception as ex:
            print('Exception publish_topics: {}'.format(ex))
