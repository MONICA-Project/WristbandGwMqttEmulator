class Settings:
    hostname = 'localhost'
    port = 1883

    interval_sending_secs = 5
    device_number = 4
    topic_prefix = "GOST/"

    number_stages = 4
    name_stages = ['WoodsTower Main', 'WoodsTower Saint Denis', 'WoodsTower Chapiteau', 'WoodsTower Woodsflor']
    people_distrib_per_stage = [25, 25, 25, 25]

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


class PermanentSettings:
    just_one_time_execution = 0
    flag_connected = 0
    list_events_publish = list()

    client_id = "mqtt_wb_simulator"
    job_id = "publish_mqtt_scral_observables"

    device_name = "GeoTag"
    device = "Wristband"
    property = "Localization"
