class Settings:
    list_events_publish = list()
    flag_connected = 0
    job_id = 'publish_mqtt_scral_observables'
    just_one_time_execution = 0

    hostname = 'localhost'
    port = 1883
    client_id = 'mqtt_wb_simulator'

    interval_sending_secs = 7
    device_number = 5
    device_name = "GeoTag"
    topic_prefix = "GOST/"
    device = "Wristband"
    property = "Localization"

    number_stages = 4
    name_stages = ['WoodsTower Main', 'WoodsTower Saint Denis', 'WoodsTower Chapiteau', 'WoodsTower Woodsflor']
    people_distrib_per_stage = [50, 25, 10, 15]

    lat_stages = [45.797197, 45.797434, 45.797425, 45.798159]
    lon_stages = [4.952072, 4.952652, 4.950973, 4.952864]

    cov_stages = [[[400, 0],
                   [0, 400]],
                  [[400, 0],
                   [0, 400]],
                  [[400, 0],
                   [0, 400]],
                  [[400, 0],
                   [0, 400]]]

    # cov_stages = [[[1, 0], [0, 1]], [[1, 0], [0, 1]], [[1, 0], [0, 1]], [[1, 0], [0, 1]]]


class RemoteSettings:
    list_events_publish = list()
    flag_connected = 0
    job_id = 'publish_mqtt_scral_observables'
    just_one_time_execution = 1

    # hostname_wp3 = "monappdwp3.monica-cloud.eu"
    hostname = 'monapp-lst.monica-cloud.eu'
    # hostname_rab = 'mpclsifrmq01.monica-cloud.eu'
    port = 1884
    client_id = 'mqtt_wb_simulator'

    interval_sending_secs = 5
    device_number = 10
    device_name = "GeoTag"
    # topic_prefix = "GOST_WOODSTOWER/"
    topic_prefix_lst = "GOST_LARGE_SCALE_TEST/"
    device = "Wristband"
    property = "Localization"