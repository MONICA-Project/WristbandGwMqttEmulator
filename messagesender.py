import os
import logging
import numpy as np
import pymap3d

from observables import Localization
from mqtt_publisher import ServerMQTT
from settings import Settings, PermanentSettings
import constants


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
    def publish_topics(dictionary_observables: dict) -> object:
        name_stages = []
        people_distrib_per_stage = []
        lat_stages = []
        lon_stages = []
        cov_stages = []

        if PermanentSettings.debug:
            device_number = Settings.device_number

            stage_number = Settings.stage_number
            name_stages = Settings.name_stages
            people_distrib_per_stage = Settings.people_distrib_per_stage

            lat_stages = Settings.lat_stages
            lon_stages = Settings.lon_stages
            cov_stages = Settings.cov_stages
        else:
            stage_number = 4
            try:
                device_number = int(os.environ[constants.DEVICE_NUMBER_KEY])

                for i in range(1, stage_number+1):
                    stage_id = "_"+str(i)
                    name_stages.append(os.environ[constants.STAGE_NAME_KEY + stage_id])
                    people_distrib_per_stage.append(float(os.environ[constants.DISTR_STAGE_KEY + stage_id]))
                    lat_stages.append(float(os.environ[constants.LAT_STAGE_KEY + stage_id]))
                    lon_stages.append(float(os.environ[constants.LON_STAGE_KEY + stage_id]))

                    cov_stages.append([
                        [int(os.environ[constants.SIGMA_N_S_KEY + stage_id]), 0],
                        [0, int(os.environ[constants.SIGMA_E_O_KEY + stage_id])]
                    ])

            except KeyError as ke:
                logging.critical("Missing environmental variable: "+str(ke))
                exit(1)

        try:
            if not dictionary_observables:
                return

            # create an ellipsoid object
            ell_wgs84 = pymap3d.Ellipsoid('wgs84')

            counter_message_sent = 0
            num_people = []

            for percentage in people_distrib_per_stage:
                num_people.append(round(percentage/100 * device_number))
            logging.debug("Total number of people: " + str(sum(num_people)))

            count = num_people[0]
            thresholds = [num_people[0]]
            for i in range(1, stage_number):
                thresholds.append(num_people[i] + count)
                count = thresholds[i]

            index_stage = 0
            current_threshold = thresholds[index_stage]

            for iot_id in dictionary_observables:
                list_topic_tag_id = dictionary_observables[iot_id]

                if len(list_topic_tag_id) < 2:
                    logging.debug("Element ignored: " + str(list_topic_tag_id))
                    continue

                topic = list_topic_tag_id[0]
                tag_id = list_topic_tag_id[1]

                cov = cov_stages[index_stage]
                # cov = [[100, 0], [0, 100]]  # diagonal covariance
                mean = [0, 0]

                num_samples = 1
                e1, n1 = np.random.multivariate_normal(mean, cov, num_samples).T
                u1 = 0

                lat0 = lat_stages[index_stage]
                lon0 = lon_stages[index_stage]
                h0 = 0
                # lat0, lon0, h0 = 5.0, 48.0, 10.0  # origin of ENU, (h is height above ellipsoid)
                # e1, n1, u1 = 0.0, 0.0, 0.0  # ENU coordinates of test point, `point_1`
                # From ENU to geodetic computation
                lat1, lon1, h1 = pymap3d.enu2geodetic(e1[0], n1[0], u1,
                                                      lat0, lon0, h0,
                                                      ell=ell_wgs84, deg=True)  # use wgs84 ellisoid

                localization = Localization(tag_id=tag_id, iot_id=iot_id, lat=lat1, lon=lon1,
                                            area_id=name_stages[index_stage])
                payload = localization.to_dictionary()
                correctly_sent = ServerMQTT.publish(topic=topic, dictionary=payload)
                if correctly_sent:
                    logging.debug('On topic: "'+topic+'" was sent payload: \n'+str(payload))
                else:
                    logging.error("Error sending on topic: '"+topic+"' payload: \n"+str(payload))

                counter_message_sent += 1

                if counter_message_sent >= current_threshold:
                    index_stage = index_stage + 1
                    if index_stage < stage_number:
                        current_threshold = thresholds[index_stage]
                    else:
                        index_stage = index_stage - 1
                        # go back -- do not increase this index larger than index_stage - 1

                if (counter_message_sent % 100) == 0:
                    logging.info('MQTT Publish Messages: {}'.format(counter_message_sent))

            logging.info('MQTT Publish Messages Completed: {}'.format(counter_message_sent))

        except Exception as ex:
            logging.error('Exception publish_topics: {}'.format(ex))
