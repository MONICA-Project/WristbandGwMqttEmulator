from observables import Localization
from mqtt_publisher import ServerMQTT


class Publisher(object):
    @staticmethod
    def publish_topics(dictionary_observables: dict, hostname: str, client_id: str, port: int):
        try:
            if not dictionary_observables:
                return

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
                ServerMQTT.publish(hostname=hostname,
                                   client_id=client_id,
                                   port=port,
                                   topic=topic,
                                   dictionary=localization.to_dictionary())
        except Exception as ex:
            print('Exception publish_topics: {}'.format(ex))
