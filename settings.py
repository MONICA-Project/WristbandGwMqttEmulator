class Settings:
    list_events_publish = list()
    flag_connected = 0
    job_id = 'publish_mqtt_scral_observables'
    just_one_time_execution = 1

    hostname = 'mpclsifrmq01.monica-cloud.eu'
    port = 1883
    client_id = 'mqtt_wb_simulator'

    interval_sending_secs = 5
    device_number = 10000
    device_name = "GeoTag"
    topic_prefix = "GOST_LARGE_SCALE_TEST/"
    device = "Wristband"
    property = "Localization"


class LocalSettings:
    list_events_publish = list()
    flag_connected = 0
    job_id = 'publish_mqtt_scral_observables'
    just_one_time_execution = 1

    hostname = 'localhost'
    port = 1884
    client_id = 'mqtt_wb_simulator'

    interval_sending_secs = 5
    device_number = 1200
    device_name = "GeoTag"
    topic_prefix = "GOST/"
    device = "Wristband"
    property = "Localization"
