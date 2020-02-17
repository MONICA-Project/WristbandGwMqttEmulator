import numpy as np
import pymap3d

from observables import Localization
from mqtt_publisher import ServerMQTT
from settings import Settings


class Publisher(object):

    class Woodstower(object):
        lat: float = 45.797549
        lon: float = 4.952724

    class Tivoli(object):
        lat: float = 55.67298336627162
        lon: float = 12.56703788516

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
    def publish_topics(dictionary_observables: dict) -> object:
        try:
            if not dictionary_observables:
                return

            # create an ellipsoid object
            ell_wgs84 = pymap3d.Ellipsoid('wgs84')

            counter_message_sent = 0
            num_people = []

            for percentage in Settings.people_distrib_per_stage:
                num_people.append(round(percentage/100 * Settings.device_number))
            # print("Total number of people: " + str(sum(num_people)))

            count = num_people[0]
            thresholds = [num_people[0]]
            for i in range(1, Settings.number_stages):
                thresholds.append(num_people[i] + count)
                count = thresholds[i]

            index_stage = 0
            current_threshold = thresholds[index_stage]

            for iot_id in dictionary_observables:
                list_topic_tag_id = dictionary_observables[iot_id]

                if len(list_topic_tag_id) < 2:
                    print("Element ignored: " + str(list_topic_tag_id))
                    continue

                topic = list_topic_tag_id[0]
                tag_id = list_topic_tag_id[1]

                cov = Settings.cov_stages[index_stage]
                # cov = [[100, 0], [0, 100]]  # diagonal covariance
                mean = [0, 0]

                num_samples = 1
                e1, n1 = np.random.multivariate_normal(mean, cov, num_samples).T
                u1 = 0

                lat0 = Settings.lat_stages[index_stage]
                lon0 = Settings.lon_stages[index_stage]
                h0 = 0
                # lat0, lon0, h0 = 5.0, 48.0, 10.0  # origin of ENU, (h is height above ellipsoid)
                # e1, n1, u1 = 0.0, 0.0, 0.0  # ENU coordinates of test point, `point_1`
                # From ENU to geodetic computation
                lat1, lon1, h1 = pymap3d.enu2geodetic(e1[0], n1[0], u1,
                                                      lat0, lon0, h0,
                                                      ell=ell_wgs84, deg=True)  # use wgs84 ellisoid

                localization = Localization(tag_id=tag_id,
                                            iot_id=iot_id,
                                            lat=lat1,
                                            lon=lon1,
                                            area_id=Settings.name_stages[index_stage])
                ServerMQTT.publish(topic=topic,
                                   dictionary=localization.to_dictionary())

                counter_message_sent += 1

                if counter_message_sent >= current_threshold:
                    index_stage = index_stage + 1
                    if index_stage < Settings.number_stages:
                        current_threshold = thresholds[index_stage]
                    else:
                        index_stage = index_stage - 1
                        # go back -- do not increase this index larger than index_stage - 1

                if (counter_message_sent % 100) == 0:
                    print('MQTT Publish Messages: {}'.format(counter_message_sent))

            print('MQTT Publish Messages Completed: {}'.format(counter_message_sent))
        except Exception as ex:
            print('Exception publish_topics: {}'.format(ex))
